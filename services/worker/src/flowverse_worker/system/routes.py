from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel, ConfigDict

from flowverse_worker.health.protocols import DependencyProbe

router = APIRouter(prefix="/internal/v1/system", tags=["internal-system"])


class WorkerStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    service: Literal["flowverse-worker"] = "flowverse-worker"
    status: Literal["ready", "unavailable"]
    reason: Literal["ready", "configuration", "timeout", "probe_failure"]


def _probe(request: Request) -> DependencyProbe:
    return request.app.state.postgres_probe


@router.get(
    "/status",
    response_model=WorkerStatusResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": WorkerStatusResponse}},
)
async def worker_status(request: Request, response: Response) -> WorkerStatusResponse:
    result = await _probe(request).check()
    if result.status != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return WorkerStatusResponse(status=result.status, reason=result.reason)
