"""HTTP health endpoint tests."""

from unittest.mock import AsyncMock


async def test_health_endpoints_return_success(client) -> None:
    for path in ("/health", "/api/v1/health"):
        response = await client.get(path)

        assert response.status_code == 200
        assert response.headers["X-Request-ID"]

        payload = response.json()
        assert payload["success"] is True
        assert payload["data"]["status"] == "ok"
        assert payload["data"]["service"] == "Verse Agent"
        assert payload["data"]["environment"] == "local"


async def test_readiness_endpoints_return_success_when_dependencies_are_ready(app, client) -> None:
    app.state.container.database.ping = AsyncMock(return_value=True)
    app.state.container.redis.ping = AsyncMock(return_value=True)

    for path in ("/ready", "/api/v1/ready"):
        response = await client.get(path)

        assert response.status_code == 200
        payload = response.json()
        assert payload["data"]["status"] == "ready"
        assert {check["name"] for check in payload["data"]["checks"]} == {"database", "redis"}


async def test_readiness_returns_service_unavailable_when_a_dependency_fails(app, client) -> None:
    app.state.container.database.ping = AsyncMock(return_value=True)
    app.state.container.redis.ping = AsyncMock(side_effect=RuntimeError("redis unavailable"))

    response = await client.get("/api/v1/ready")

    assert response.status_code == 503
    payload = response.json()
    assert payload["data"]["status"] == "degraded"
    assert any(check["status"] == "error" for check in payload["data"]["checks"])
