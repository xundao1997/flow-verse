from __future__ import annotations

import asyncio
from typing import Literal

from flowverse_worker.cli import (
    EXIT_CONFIGURATION,
    EXIT_DEPENDENCY,
    EXIT_OK,
    check_dependencies,
)
from flowverse_worker.core.settings import Settings
from flowverse_worker.health.protocols import ProbeResult


class FakeProbe:
    def __init__(
        self,
        status: Literal["ready", "unavailable"],
        reason: Literal["ready", "configuration", "timeout", "probe_failure"],
    ) -> None:
        self.result = ProbeResult(status=status, reason=reason)
        self.closed = False

    async def check(self) -> ProbeResult:
        return self.result

    async def close(self) -> None:
        self.closed = True


def test_worker_check_succeeds_and_closes_probe() -> None:
    probe = FakeProbe("ready", "ready")

    exit_code = asyncio.run(check_dependencies(Settings(), postgres_probe=probe))

    assert exit_code == EXIT_OK
    assert probe.closed is True


def test_worker_check_reports_invalid_configuration() -> None:
    exit_code = asyncio.run(
        check_dependencies(
            Settings(),
            postgres_probe=FakeProbe("unavailable", "configuration"),
        )
    )

    assert exit_code == EXIT_CONFIGURATION


def test_worker_check_distinguishes_dependency_failure() -> None:
    exit_code = asyncio.run(
        check_dependencies(
            Settings(),
            postgres_probe=FakeProbe("unavailable", "probe_failure"),
        )
    )

    assert exit_code == EXIT_DEPENDENCY
