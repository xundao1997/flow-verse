# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnusedFunction=false
from __future__ import annotations

from fastapi.testclient import TestClient
from httpx import Response

from flowverse_worker.api.main import create_app
from flowverse_worker.core.settings import Settings
from flowverse_worker.health.protocols import ProbeResult


class FakeProbe:
    def __init__(self, result: ProbeResult) -> None:
        self.result = result
        self.closed = False

    async def check(self) -> ProbeResult:
        return self.result

    async def close(self) -> None:
        self.closed = True


def test_worker_status_is_ready_only_when_postgres_is_ready() -> None:
    probe = FakeProbe(ProbeResult(status="ready", reason="ready"))
    app = create_app(settings=Settings(), postgres_probe=probe)

    with TestClient(app) as client:
        response: Response = client.get(
            "/internal/v1/system/status",
            headers={"x-request-id": "worker-ready"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "service": "flowverse-worker",
        "status": "ready",
        "reason": "ready",
    }
    assert response.headers["x-request-id"] == "worker-ready"
    assert len(response.headers["x-trace-id"]) == 32
    assert probe.closed is True


def test_worker_status_is_unavailable_when_postgres_is_unavailable() -> None:
    probe = FakeProbe(ProbeResult(status="unavailable", reason="timeout"))
    app = create_app(settings=Settings(), postgres_probe=probe)

    with TestClient(app) as client:
        response: Response = client.get("/internal/v1/system/status")

    assert response.status_code == 503
    assert response.json() == {
        "service": "flowverse-worker",
        "status": "unavailable",
        "reason": "timeout",
    }


def test_unhandled_worker_error_keeps_correlation_headers() -> None:
    probe = FakeProbe(ProbeResult(status="ready", reason="ready"))
    app = create_app(settings=Settings(), postgres_probe=probe)

    @app.get("/test/error")
    async def error_route() -> None:
        raise RuntimeError("test error")

    with TestClient(app, raise_server_exceptions=False) as client:
        response: Response = client.get(
            "/test/error",
            headers={"x-request-id": "worker-error"},
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
    assert response.headers["x-request-id"] == "worker-error"
    assert len(response.headers["x-trace-id"]) == 32
