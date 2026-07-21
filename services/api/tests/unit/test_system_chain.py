# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnusedFunction=false
from __future__ import annotations

from fastapi.testclient import TestClient
from httpx import Response

from flowverse_api.api.main import create_app
from flowverse_api.core.settings import Settings
from flowverse_api.health.protocols import ProbeResult
from flowverse_api.system.protocols import WorkerProbeResult


class ReadyPostgresProbe:
    async def check(self) -> ProbeResult:
        return ProbeResult(status="ready", reason="ready")

    async def close(self) -> None:
        return None


class UnavailablePostgresProbe:
    async def check(self) -> ProbeResult:
        return ProbeResult(status="unavailable", reason="configuration")

    async def close(self) -> None:
        return None


class FakeWorkerClient:
    def __init__(self, result: WorkerProbeResult) -> None:
        self.result = result
        self.request_ids: list[str] = []
        self.closed = False

    async def ping(self, *, request_id: str) -> WorkerProbeResult:
        self.request_ids.append(request_id)
        return self.result

    async def close(self) -> None:
        self.closed = True


def test_chain_reports_api_and_worker_ready() -> None:
    worker = FakeWorkerClient(WorkerProbeResult(status="ready", reason="ready"))
    app = create_app(
        settings=Settings(),
        postgres_probe=ReadyPostgresProbe(),
        worker_client=worker,
    )

    with TestClient(app) as client:
        response: Response = client.get(
            "/api/v1/system/chain",
            headers={"x-request-id": "chain-test"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "services": {
            "api": {"status": "ready", "reason": "ready"},
            "worker": {"status": "ready", "reason": "ready"},
        },
    }
    assert worker.request_ids == ["chain-test"]
    assert worker.closed is True


def test_chain_returns_503_when_worker_is_unavailable() -> None:
    worker = FakeWorkerClient(WorkerProbeResult(status="unavailable", reason="connection"))
    app = create_app(
        settings=Settings(),
        postgres_probe=ReadyPostgresProbe(),
        worker_client=worker,
    )

    with TestClient(app) as client:
        response: Response = client.get("/api/v1/system/chain")

    assert response.status_code == 503
    assert response.json()["status"] == "degraded"
    assert response.json()["services"]["worker"] == {
        "status": "unavailable",
        "reason": "connection",
    }


def test_chain_returns_503_when_api_postgres_is_unavailable() -> None:
    worker = FakeWorkerClient(WorkerProbeResult(status="ready", reason="ready"))
    app = create_app(
        settings=Settings(),
        postgres_probe=UnavailablePostgresProbe(),
        worker_client=worker,
    )

    with TestClient(app) as client:
        response: Response = client.get("/api/v1/system/chain")

    assert response.status_code == 503
    assert response.json()["status"] == "degraded"
    assert response.json()["services"]["api"] == {
        "status": "unavailable",
        "reason": "configuration",
    }


def test_unhandled_error_response_keeps_correlation_headers() -> None:
    worker = FakeWorkerClient(WorkerProbeResult(status="ready", reason="ready"))
    app = create_app(
        settings=Settings(),
        postgres_probe=ReadyPostgresProbe(),
        worker_client=worker,
    )

    @app.get("/test/error")
    async def error_route() -> None:
        raise RuntimeError("test error")

    with TestClient(app, raise_server_exceptions=False) as client:
        response: Response = client.get(
            "/test/error",
            headers={"x-request-id": "error-test"},
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
    assert response.headers["x-request-id"] == "error-test"
    assert len(response.headers["x-trace-id"]) == 32
