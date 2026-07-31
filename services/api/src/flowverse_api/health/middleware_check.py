from __future__ import annotations

import asyncio
import hashlib
import hmac
import ipaddress
import sys
from contextlib import suppress
from datetime import UTC, datetime
from urllib.parse import quote, urlsplit, urlunsplit

import httpx

from flowverse_api.core.settings import Settings
from flowverse_api.health.postgres import PostgresProbe
from flowverse_api.health.protocols import ProbeResult

_EMPTY_PAYLOAD_HASH = hashlib.sha256(b"").hexdigest()
_SIGNED_HEADERS = "host;x-amz-content-sha256;x-amz-date"


def _is_loopback_host(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _redis_command(*parts: str) -> bytes:
    encoded = [part.encode("utf-8") for part in parts]
    chunks = [f"*{len(encoded)}\r\n".encode()]
    for part in encoded:
        chunks.extend((f"${len(part)}\r\n".encode(), part, b"\r\n"))
    return b"".join(chunks)


async def _read_redis_simple_reply(reader: asyncio.StreamReader, expected: bytes) -> None:
    line = await reader.readline()
    if line != b"+" + expected + b"\r\n":
        raise RuntimeError("Redis returned an unexpected response")


async def check_redis(settings: Settings) -> ProbeResult:
    if settings.redis_password is None or not _is_loopback_host(settings.redis_host):
        return ProbeResult(status="unavailable", reason="configuration")

    writer: asyncio.StreamWriter | None = None
    try:
        async with asyncio.timeout(settings.middleware_probe_timeout_seconds):
            reader, writer = await asyncio.open_connection(
                settings.redis_host,
                settings.redis_port,
            )
            password = settings.redis_password.get_secret_value()
            writer.write(_redis_command("AUTH", password) + _redis_command("PING"))
            await writer.drain()
            await _read_redis_simple_reply(reader, b"OK")
            await _read_redis_simple_reply(reader, b"PONG")
    except TimeoutError:
        return ProbeResult(status="unavailable", reason="timeout")
    except Exception:
        return ProbeResult(status="unavailable", reason="probe_failure")
    finally:
        if writer is not None:
            writer.close()
            with suppress(OSError):
                await writer.wait_closed()

    return ProbeResult(status="ready", reason="ready")


def _sign(key: bytes, message: str) -> bytes:
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()


def build_minio_list_buckets_request(
    settings: Settings,
    *,
    now: datetime | None = None,
) -> tuple[str, dict[str, str]] | None:
    if (
        settings.minio_endpoint is None
        or settings.minio_access_key is None
        or settings.minio_secret_key is None
    ):
        return None

    endpoint = urlsplit(str(settings.minio_endpoint))
    if (
        endpoint.scheme not in {"http", "https"}
        or endpoint.hostname is None
        or not _is_loopback_host(endpoint.hostname)
        or endpoint.username is not None
        or endpoint.password is not None
        or endpoint.query
        or endpoint.fragment
        or endpoint.path not in {"", "/"}
    ):
        return None

    request_time = (now or datetime.now(UTC)).astimezone(UTC)
    amz_date = request_time.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = request_time.strftime("%Y%m%d")
    canonical_uri = quote(endpoint.path or "/", safe="/-_.~")
    host = endpoint.netloc
    canonical_headers = (
        f"host:{host}\nx-amz-content-sha256:{_EMPTY_PAYLOAD_HASH}\nx-amz-date:{amz_date}\n"
    )
    canonical_request = "\n".join(
        (
            "GET",
            canonical_uri,
            "",
            canonical_headers,
            _SIGNED_HEADERS,
            _EMPTY_PAYLOAD_HASH,
        )
    )
    scope = f"{date_stamp}/{settings.minio_region}/s3/aws4_request"
    string_to_sign = "\n".join(
        (
            "AWS4-HMAC-SHA256",
            amz_date,
            scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        )
    )
    secret_key = settings.minio_secret_key.get_secret_value()
    signing_key = _sign(
        _sign(
            _sign(
                _sign(("AWS4" + secret_key).encode("utf-8"), date_stamp),
                settings.minio_region,
            ),
            "s3",
        ),
        "aws4_request",
    )
    signature = hmac.new(
        signing_key,
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    access_key = settings.minio_access_key.get_secret_value()
    authorization = (
        "AWS4-HMAC-SHA256 "
        f"Credential={access_key}/{scope}, "
        f"SignedHeaders={_SIGNED_HEADERS}, "
        f"Signature={signature}"
    )
    request_url = urlunsplit((endpoint.scheme, endpoint.netloc, canonical_uri, "", ""))
    return request_url, {
        "Authorization": authorization,
        "Host": host,
        "x-amz-content-sha256": _EMPTY_PAYLOAD_HASH,
        "x-amz-date": amz_date,
    }


async def check_minio(
    settings: Settings,
    *,
    transport: httpx.AsyncBaseTransport | None = None,
) -> ProbeResult:
    request = build_minio_list_buckets_request(settings)
    if request is None:
        return ProbeResult(status="unavailable", reason="configuration")

    request_url, headers = request
    try:
        async with httpx.AsyncClient(
            timeout=settings.middleware_probe_timeout_seconds,
            transport=transport,
            trust_env=False,
        ) as client:
            response = await client.get(request_url, headers=headers)
    except httpx.TimeoutException:
        return ProbeResult(status="unavailable", reason="timeout")
    except httpx.HTTPError:
        return ProbeResult(status="unavailable", reason="probe_failure")

    if response.status_code != 200:
        return ProbeResult(status="unavailable", reason="probe_failure")
    return ProbeResult(status="ready", reason="ready")


async def check_postgres(settings: Settings) -> ProbeResult:
    probe = PostgresProbe(settings)
    try:
        return await probe.check()
    finally:
        await probe.close()


async def run_checks(settings: Settings) -> dict[str, ProbeResult]:
    postgres, redis, minio = await asyncio.gather(
        check_postgres(settings),
        check_redis(settings),
        check_minio(settings),
    )
    return {"PostgreSQL": postgres, "Redis": redis, "MinIO": minio}


def main() -> int:
    loop_factory = asyncio.SelectorEventLoop if sys.platform == "win32" else None
    results = asyncio.run(run_checks(Settings()), loop_factory=loop_factory)
    print("FlowVerse local middleware authentication check")
    for name, result in results.items():
        print(f"  {name}: {result.status} ({result.reason})")
    if all(result.status == "ready" for result in results.values()):
        print("All three middleware services are authenticated and reachable.")
        return 0
    print("One or more middleware services are unavailable.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
