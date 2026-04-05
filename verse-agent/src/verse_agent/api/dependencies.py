"""Reusable FastAPI dependencies."""

from collections.abc import AsyncIterator
from typing import cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from verse_agent.cache.redis_client import RedisClient
from verse_agent.core.config import AppSettings
from verse_agent.core.container import AppContainer


def get_container(request: Request) -> AppContainer:
    """Return the application dependency container."""
    return cast(AppContainer, request.app.state.container)


def get_settings(container: AppContainer = Depends(get_container)) -> AppSettings:
    """Expose application settings through dependency injection."""
    return container.settings


async def get_db_session(
    container: AppContainer = Depends(get_container),
) -> AsyncIterator[AsyncSession]:
    """Yield an async database session."""
    async for session in container.database.get_session():
        yield session


def get_redis_client(
    container: AppContainer = Depends(get_container),
) -> RedisClient:
    """Expose the Redis adapter through dependency injection."""
    return container.redis
