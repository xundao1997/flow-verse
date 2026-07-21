# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false
from __future__ import annotations

from typing import Literal

from fastapi.testclient import TestClient
from httpx import Response
from pydantic import SecretStr

from flowverse_api.api.main import create_app
from flowverse_api.core.settings import Settings
from flowverse_api.health.protocols import ProbeResult


class FakeProbe:
    def __init__(self, status: Literal["ready", "unavailable"]) -> None:
        self.status = status
        self.check_count = 0
        self.closed = False

    async def check(self) -> ProbeResult:
        self.check_count += 1
        if self.status == "ready":
            return ProbeResult(status="ready", reason="ready")
        return ProbeResult(status="unavailable", reason="probe_failure")

    async def close(self) -> None:
        self.closed = True


def test_liveness_does_not_probe_dependencies() -> None:
    probe = FakeProbe("unavailable")
    app = create_app(settings=Settings(), postgres_probe=probe)

    with TestClient(app) as client:
        response: Response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
    assert probe.check_count == 0
    assert probe.closed is True


def test_readiness_is_503_when_postgres_is_unavailable() -> None:
    app = create_app(settings=Settings(), postgres_probe=FakeProbe("unavailable"))

    with TestClient(app) as client:
        response: Response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}


def test_readiness_is_200_when_postgres_is_ready() -> None:
    app = create_app(settings=Settings(), postgres_probe=FakeProbe("ready"))

    with TestClient(app) as client:
        response: Response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_dependencies_contract_reports_deferred_object_storage() -> None:
    app = create_app(settings=Settings(), postgres_probe=FakeProbe("ready"))

    with TestClient(app) as client:
        response: Response = client.get("/health/dependencies")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "dependencies": {
            "postgres": {"status": "ready"},
            "object_storage": {"status": "deferred"},
        },
    }


def test_dependencies_contract_degrades_without_leaking_configuration() -> None:
    secret = "postgresql+psycopg://user:do-not-leak@db.example/flowverse"
    settings = Settings(database_url=SecretStr(secret))
    app = create_app(settings=settings, postgres_probe=FakeProbe("unavailable"))

    with TestClient(app) as client:
        response: Response = client.get("/health/dependencies")

    assert response.status_code == 200
    assert response.json() == {
        "status": "degraded",
        "dependencies": {
            "postgres": {"status": "unavailable"},
            "object_storage": {"status": "deferred"},
        },
    }
    assert secret not in response.text


def test_request_context_headers_are_returned_and_invalid_input_is_replaced() -> None:
    app = create_app(settings=Settings(), postgres_probe=FakeProbe("ready"))

    with TestClient(app) as client:
        response: Response = client.get("/health/live", headers={"x-request-id": "invalid value"})

    assert response.headers["x-request-id"] != "invalid value"
    assert len(response.headers["x-trace-id"]) == 32
