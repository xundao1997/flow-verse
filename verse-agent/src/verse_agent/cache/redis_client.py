"""Redis adapter with a narrow, typed interface."""

from typing import TypeAlias

import redis.asyncio as redis
from redis.asyncio.client import Redis

from verse_agent.core.config import RedisSettings

RedisValue: TypeAlias = str | bytes | int | float


class RedisClient:
    """Encapsulate Redis access for caching and small key-value operations."""

    def __init__(self, settings: RedisSettings) -> None:
        self._settings = settings
        self._client: Redis | None = None

    def _build_client(self) -> Redis:
        return redis.from_url(
            self._settings.url,
            encoding="utf-8",
            decode_responses=self._settings.decode_responses,
            socket_timeout=self._settings.socket_timeout,
            health_check_interval=self._settings.health_check_interval,
        )

    async def get_client(self) -> Redis:
        """Create the Redis client lazily."""
        if self._client is None:
            self._client = self._build_client()
        return self._client

    async def get(self, key: str) -> str | None:
        """Get a string value by key."""
        client = await self.get_client()
        value = await client.get(key)
        if value is None:
            return None
        return str(value)

    async def set(
        self,
        key: str,
        value: RedisValue,
        expire_seconds: int | None = None,
    ) -> bool:
        """Set a key with an optional TTL."""
        client = await self.get_client()
        return bool(await client.set(key, value, ex=expire_seconds))

    async def delete(self, key: str) -> int:
        """Delete a key and return the number of removed entries."""
        client = await self.get_client()
        return int(await client.delete(key))

    async def ping(self) -> bool:
        """Probe Redis availability."""
        client = await self.get_client()
        return bool(await client.ping())

    async def close(self) -> None:
        """Close the Redis client if it has been created."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
