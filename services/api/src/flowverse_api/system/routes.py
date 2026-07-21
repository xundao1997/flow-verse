from __future__ import annotations

import asyncio

from fastapi import APIRouter, Request, Response, status

from flowverse_api.health.protocols import DependencyProbe
from flowverse_api.system.models import ChainResponse, ChainServices, ServiceState
from flowverse_api.system.protocols import WorkerClient

router = APIRouter(prefix="/api/v1/system", tags=["system"])


def _worker_client(request: Request) -> WorkerClient:
    return request.app.state.worker_client


def _postgres_probe(request: Request) -> DependencyProbe:
    return request.app.state.postgres_probe


@router.get(
    "/chain",
    response_model=ChainResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ChainResponse}},
)
async def chain(request: Request, response: Response) -> ChainResponse:
    api_result, worker_result = await asyncio.gather(
        _postgres_probe(request).check(),
        _worker_client(request).ping(request_id=request.state.request_id),
    )
    api = ServiceState(status=api_result.status, reason=api_result.reason)
    worker = ServiceState(status=worker_result.status, reason=worker_result.reason)
    if api_result.status != "ready" or worker_result.status != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ChainResponse(
            status="degraded",
            services=ChainServices(api=api, worker=worker),
        )
    return ChainResponse(
        status="ready",
        services=ChainServices(api=api, worker=worker),
    )
