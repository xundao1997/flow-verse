from __future__ import annotations

import asyncio

import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from flowverse_worker.core.settings import Settings
from flowverse_worker.health.protocols import ProbeResult

_LOGGER = structlog.get_logger("flowverse_worker.health.postgres")
_SUPPORTED_PREFIXES = ("postgresql+psycopg://", "postgresql+psycopg_async://")


class PostgresProbe:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine: AsyncEngine | None = None

    def _database_url(self) -> str | None:
        if self._settings.database_url is None:
            return None
        value = self._settings.database_url.get_secret_value()
        if not value.startswith(_SUPPORTED_PREFIXES):
            return None
        return value

    def _get_engine(self, database_url: str) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(database_url, pool_pre_ping=False)
        return self._engine

    async def check(self) -> ProbeResult:
        database_url = self._database_url()
        if database_url is None:
            _LOGGER.warning("postgres_probe_unavailable", reason="configuration")
            return ProbeResult(status="unavailable", reason="configuration")

        try:
            async with asyncio.timeout(self._settings.postgres_probe_timeout_seconds):
                async with self._get_engine(database_url).connect() as connection:
                    await connection.execute(text("SELECT 1"))
        except TimeoutError:
            _LOGGER.warning("postgres_probe_unavailable", reason="timeout")
            return ProbeResult(status="unavailable", reason="timeout")
        except Exception as exc:
            _LOGGER.warning(
                "postgres_probe_unavailable",
                reason="probe_failure",
                error_type=type(exc).__name__,
            )
            return ProbeResult(status="unavailable", reason="probe_failure")

        return ProbeResult(status="ready", reason="ready")

    async def close(self) -> None:
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
