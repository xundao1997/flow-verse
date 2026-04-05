"""Tests for the Redis adapter."""

from unittest.mock import AsyncMock

from verse_agent.cache.redis_client import RedisClient
from verse_agent.core.config import RedisSettings


async def test_redis_client_methods_delegate_to_backend() -> None:
    redis_client = RedisClient(RedisSettings())
    backend = AsyncMock()
    backend.get.return_value = "cached-value"
    backend.set.return_value = True
    backend.delete.return_value = 1
    redis_client._client = backend

    assert await redis_client.get("sample-key") == "cached-value"
    assert await redis_client.set("sample-key", "payload", expire_seconds=60) is True
    assert await redis_client.delete("sample-key") == 1

    backend.get.assert_awaited_once_with("sample-key")
    backend.set.assert_awaited_once_with("sample-key", "payload", ex=60)
    backend.delete.assert_awaited_once_with("sample-key")
