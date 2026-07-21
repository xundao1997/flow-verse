from __future__ import annotations

import asyncio

import httpx

from flowverse_api.core.settings import Settings
from flowverse_api.system.worker import HttpxWorkerClient


def run_ping(handler: httpx.MockTransport) -> tuple[str, str]:
    async def execute() -> tuple[str, str]:
        client = HttpxWorkerClient(Settings(), transport=handler)
        try:
            result = await client.ping(request_id="worker-client-test")
            return result.status, result.reason
        finally:
            await client.close()

    return asyncio.run(execute())


def test_worker_client_accepts_dependency_ready_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/internal/v1/system/status"
        assert request.headers["x-request-id"] == "worker-client-test"
        return httpx.Response(
            200,
            json={
                "service": "flowverse-worker",
                "status": "ready",
                "reason": "ready",
            },
        )

    assert run_ping(httpx.MockTransport(handler)) == ("ready", "ready")


def test_worker_client_preserves_worker_dependency_reason() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            503,
            json={
                "service": "flowverse-worker",
                "status": "unavailable",
                "reason": "timeout",
            },
        )

    assert run_ping(httpx.MockTransport(handler)) == ("unavailable", "timeout")


def test_worker_client_rejects_status_code_schema_mismatch() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "service": "flowverse-worker",
                "status": "unavailable",
                "reason": "timeout",
            },
        )

    assert run_ping(httpx.MockTransport(handler)) == (
        "unavailable",
        "invalid_response",
    )


def test_worker_client_does_not_retry_timeout() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        raise httpx.ReadTimeout("timed out", request=request)

    assert run_ping(httpx.MockTransport(handler)) == ("unavailable", "timeout")
    assert attempts == 1
