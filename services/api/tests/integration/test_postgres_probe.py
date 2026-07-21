from __future__ import annotations

import asyncio
import os

import pytest
from pydantic import SecretStr

from flowverse_api.core.settings import Settings
from flowverse_api.health.postgres import PostgresProbe

pytestmark = pytest.mark.integration


def test_postgres_probe_against_explicit_test_database() -> None:
    database_url = os.getenv("FLOWVERSE_TEST_DATABASE_URL")
    if database_url is None:
        pytest.skip("FLOWVERSE_TEST_DATABASE_URL is not configured")

    probe = PostgresProbe(Settings(database_url=SecretStr(database_url)))

    async def run_probe() -> str:
        try:
            return (await probe.check()).status
        finally:
            await probe.close()

    assert asyncio.run(run_probe()) == "ready"
