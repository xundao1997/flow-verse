"""Application entrypoints."""

from fastapi import FastAPI
import uvicorn

from verse_agent.api.router import api_router, public_router
from verse_agent.core.config import get_settings
from verse_agent.core.exception_handlers import register_exception_handlers
from verse_agent.core.lifecycle import lifespan
from verse_agent.core.middleware import register_middleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    register_middleware(application)
    register_exception_handlers(application)
    application.include_router(public_router)
    application.include_router(api_router, prefix=settings.api_v1_prefix)
    return application


def main() -> None:
    """Run the application with uvicorn."""
    settings = get_settings()
    uvicorn.run(
        "verse_agent.main:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
