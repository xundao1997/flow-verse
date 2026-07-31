from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import httpx
from pydantic import AnyHttpUrl, SecretStr

from flowverse_api.core.settings import Settings
from flowverse_api.health.middleware_check import (
    build_minio_list_buckets_request,
    check_minio,
    check_redis,
)


def _middleware_settings() -> Settings:
    return Settings(
        redis_password=SecretStr("redis-test-secret"),
        minio_endpoint=AnyHttpUrl("http://127.0.0.1:19000"),
        minio_access_key=SecretStr("minio-test-user"),
        minio_secret_key=SecretStr("minio-test-secret"),
    )


def test_minio_request_is_signed_without_exposing_secret() -> None:
    settings = _middleware_settings()
    request = build_minio_list_buckets_request(
        settings,
        now=datetime(2026, 7, 29, 0, 0, tzinfo=UTC),
    )

    assert request is not None
    request_url, headers = request
    assert request_url == "http://127.0.0.1:19000/"
    assert (
        "Credential=minio-test-user/20260729/us-east-1/s3/aws4_request" in headers["Authorization"]
    )
    assert "minio-test-secret" not in str(headers)


def test_minio_check_requires_credentials() -> None:
    result = asyncio.run(check_minio(Settings()))

    assert result.status == "unavailable"
    assert result.reason == "configuration"


def test_minio_check_rejects_non_loopback_endpoint() -> None:
    settings = _middleware_settings().model_copy(
        update={"minio_endpoint": AnyHttpUrl("http://minio.example.com:9000")}
    )

    result = asyncio.run(check_minio(settings))

    assert result.status == "unavailable"
    assert result.reason == "configuration"


def test_minio_check_accepts_authenticated_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"].startswith("AWS4-HMAC-SHA256 ")
        return httpx.Response(200, content=b"<ListAllMyBucketsResult />")

    result = asyncio.run(
        check_minio(_middleware_settings(), transport=httpx.MockTransport(handler))
    )

    assert result.status == "ready"
    assert result.reason == "ready"


def test_redis_check_authenticates_and_pings() -> None:
    async def scenario() -> None:
        commands: list[bytes] = []

        async def handler(
            reader: asyncio.StreamReader,
            writer: asyncio.StreamWriter,
        ) -> None:
            try:
                for response in (b"+OK\r\n", b"+PONG\r\n"):
                    header = await reader.readline()
                    part_count = int(header[1:-2])
                    parts: list[bytes] = []
                    for _ in range(part_count):
                        length_line = await reader.readline()
                        length = int(length_line[1:-2])
                        parts.append(await reader.readexactly(length))
                        await reader.readexactly(2)
                    commands.append(b" ".join(parts))
                    writer.write(response)
                    await writer.drain()
            finally:
                writer.close()
                await writer.wait_closed()

        server = await asyncio.start_server(handler, "127.0.0.1", 0)
        try:
            socket = server.sockets[0]
            port = int(socket.getsockname()[1])
            settings = Settings(
                redis_host="127.0.0.1",
                redis_port=port,
                redis_password=SecretStr("redis-test-secret"),
            )
            result = await check_redis(settings)
        finally:
            server.close()
            await server.wait_closed()

        assert result.status == "ready"
        assert commands == [b"AUTH redis-test-secret", b"PING"]

    asyncio.run(scenario())


def test_redis_check_requires_password() -> None:
    result = asyncio.run(check_redis(Settings()))

    assert result.status == "unavailable"
    assert result.reason == "configuration"


def test_redis_check_rejects_non_loopback_host() -> None:
    settings = Settings(
        redis_host="redis.example.com",
        redis_password=SecretStr("redis-test-secret"),
    )

    result = asyncio.run(check_redis(settings))

    assert result.status == "unavailable"
    assert result.reason == "configuration"
