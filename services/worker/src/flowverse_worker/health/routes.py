from __future__ import annotations

from fastapi import APIRouter, Request, Response, status

from flowverse_worker.health.models import LivenessResponse, ReadinessResponse
from flowverse_worker.health.protocols import DependencyProbe

router = APIRouter(prefix="/health", tags=["health"])


def _probe(request: Request) -> DependencyProbe:
    return request.app.state.postgres_probe


@router.get("/live", response_model=LivenessResponse)
async def live() -> LivenessResponse:
    return LivenessResponse()


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ReadinessResponse}},
)
async def ready(request: Request, response: Response) -> ReadinessResponse:
    result = await _probe(request).check()
    if result.status != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ReadinessResponse(status="unavailable")
    return ReadinessResponse(status="ready")
