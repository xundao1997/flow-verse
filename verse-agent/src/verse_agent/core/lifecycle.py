"""Application startup and shutdown hooks."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from verse_agent.core.config import get_settings
from verse_agent.core.container import AppContainer
from verse_agent.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize and tear down application resources."""
    settings = get_settings()
    configure_logging(settings.logging)

    container = AppContainer.from_settings(settings)
    app.state.container = container

    logger.bind(component="app").info(
        "Application initialized for environment {}", settings.app_env
    )
    try:
        yield
    finally:
        await container.shutdown()
        logger.bind(component="app").info("Application shutdown complete")
