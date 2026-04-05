"""Pytest fixtures and path bootstrapping."""

import sys
from collections.abc import AsyncIterator, Generator
from pathlib import Path

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from verse_agent.core.config import reset_settings_cache
from verse_agent.main import create_app


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Generator[None, None, None]:
    """Ensure each test sees a fresh settings snapshot."""
    reset_settings_cache()
    yield
    reset_settings_cache()


@pytest.fixture
async def app() -> AsyncIterator:
    """Create the FastAPI app with lifespan events enabled."""
    application = create_app()
    async with LifespanManager(application):
        yield application


@pytest.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    """Create an async HTTP client for the app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as async_client:
        yield async_client
