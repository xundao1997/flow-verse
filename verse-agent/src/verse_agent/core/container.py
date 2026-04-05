"""Application dependency container."""

from dataclasses import dataclass

from verse_agent.cache.redis_client import RedisClient
from verse_agent.core.config import AppSettings
from verse_agent.db.session import DatabaseManager


@dataclass(slots=True)
class AppContainer:
    """Store long-lived application dependencies."""

    settings: AppSettings
    database: DatabaseManager
    redis: RedisClient

    @classmethod
    def from_settings(cls, settings: AppSettings) -> "AppContainer":
        """Build the container from validated settings."""
        return cls(
            settings=settings,
            database=DatabaseManager(settings.database),
            redis=RedisClient(settings.redis),
        )

    async def shutdown(self) -> None:
        """Release resources created during runtime."""
        await self.database.dispose()
        await self.redis.close()
