from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from flowverse_worker.api.middleware import (
    RequestContextMiddleware,
    unhandled_exception_response,
)
from flowverse_worker.core.logging import configure_logging
from flowverse_worker.core.settings import Settings
from flowverse_worker.core.telemetry import configure_telemetry
from flowverse_worker.health.postgres import PostgresProbe
from flowverse_worker.health.protocols import DependencyProbe
from flowverse_worker.health.routes import router as health_router
from flowverse_worker.system.routes import router as system_router


def create_app(
    *,
    settings: Settings | None = None,
    postgres_probe: DependencyProbe | None = None,
) -> FastAPI:
    resolved_settings = settings or Settings()
    configure_logging(level=resolved_settings.log_level)
    configure_telemetry(service_name="flowverse-worker")
    resolved_probe = postgres_probe or PostgresProbe(resolved_settings)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        try:
            yield
        finally:
            await resolved_probe.close()

    application = FastAPI(
        title="FlowVerse Architecture Bootstrap Worker",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.state.settings = resolved_settings
    application.state.postgres_probe = resolved_probe
    application.add_middleware(RequestContextMiddleware)
    application.add_exception_handler(Exception, unhandled_exception_response)
    application.include_router(health_router)
    application.include_router(system_router)
    return application


app = create_app()
