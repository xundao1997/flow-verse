"""Health check endpoints."""

import asyncio

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from verse_agent.api.dependencies import get_container, get_settings
from verse_agent.core.config import AppSettings
from verse_agent.core.container import AppContainer
from verse_agent.schemas.common import ResponseEnvelope
from verse_agent.schemas.health import DependencyHealth, HealthPayload, ReadinessPayload

router = APIRouter(tags=["health"])
public_router = APIRouter(tags=["health"])
READINESS_TIMEOUT_SECONDS = 2.0


def build_health_payload(settings: AppSettings) -> HealthPayload:
    """Build the liveness response payload."""
    return HealthPayload(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )


async def _run_probe(name: str, operation) -> DependencyHealth:
    try:
        await asyncio.wait_for(operation(), timeout=READINESS_TIMEOUT_SECONDS)
    except TimeoutError:
        return DependencyHealth(name=name, status="error", detail="Probe timed out.")
    except Exception as exc:
        return DependencyHealth(name=name, status="error", detail=str(exc))
    return DependencyHealth(name=name, status="ok")


async def build_readiness_payload(
    settings: AppSettings,
    container: AppContainer,
) -> tuple[ReadinessPayload, int]:
    """Build the readiness response payload with dependency probes."""
    checks = await asyncio.gather(
        _run_probe("database", container.database.ping),
        _run_probe("redis", container.redis.ping),
    )
    all_ready = all(check.status == "ok" for check in checks)
    payload = ReadinessPayload(
        status="ready" if all_ready else "degraded",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        checks=checks,
    )
    status_code = status.HTTP_200_OK if all_ready else status.HTTP_503_SERVICE_UNAVAILABLE
    return payload, status_code


@router.get(
    "/health",
    response_model=ResponseEnvelope[HealthPayload],
    summary="Versioned liveness check",
)
@public_router.get(
    "/health",
    response_model=ResponseEnvelope[HealthPayload],
    summary="Liveness check",
)
async def health_check(
    settings: AppSettings = Depends(get_settings),
) -> ResponseEnvelope[HealthPayload]:
    """Return service liveness information."""
    return ResponseEnvelope(data=build_health_payload(settings))


@router.get(
    "/ready",
    response_model=ResponseEnvelope[ReadinessPayload],
    summary="Versioned readiness check",
)
@public_router.get(
    "/ready",
    response_model=ResponseEnvelope[ReadinessPayload],
    summary="Readiness check",
)
async def readiness_check(
    settings: AppSettings = Depends(get_settings),
    container: AppContainer = Depends(get_container),
) -> JSONResponse:
    """Return service readiness information, including dependency probes."""
    payload, status_code = await build_readiness_payload(settings, container)
    envelope = ResponseEnvelope(data=payload)
    return JSONResponse(status_code=status_code, content=envelope.model_dump(mode="json"))
