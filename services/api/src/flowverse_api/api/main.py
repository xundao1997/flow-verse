from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from flowverse_api.api.middleware import RequestContextMiddleware, unhandled_exception_response
from flowverse_api.core.logging import configure_logging
from flowverse_api.core.settings import Settings
from flowverse_api.core.telemetry import configure_telemetry
from flowverse_api.health.postgres import PostgresProbe
from flowverse_api.health.protocols import DependencyProbe
from flowverse_api.health.routes import router as health_router
from flowverse_api.system.protocols import WorkerClient
from flowverse_api.system.routes import router as system_router
from flowverse_api.system.worker import HttpxWorkerClient


def create_app(
    *,
    settings: Settings | None = None,
    postgres_probe: DependencyProbe | None = None,
    worker_client: WorkerClient | None = None,
) -> FastAPI:
    resolved_settings = settings or Settings()
    configure_logging(level=resolved_settings.log_level)
    configure_telemetry(service_name="flowverse-api")
    resolved_probe = postgres_probe or PostgresProbe(resolved_settings)
    resolved_worker_client = worker_client or HttpxWorkerClient(resolved_settings)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        try:
            yield
        finally:
            await asyncio.gather(resolved_probe.close(), resolved_worker_client.close())

    application = FastAPI(
        title="FlowVerse Architecture Bootstrap API",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.state.settings = resolved_settings
    application.state.postgres_probe = resolved_probe
    application.state.worker_client = resolved_worker_client
    application.add_middleware(RequestContextMiddleware)
    application.add_exception_handler(Exception, unhandled_exception_response)
    application.include_router(health_router)
    application.include_router(system_router)
    return application


app = create_app()
