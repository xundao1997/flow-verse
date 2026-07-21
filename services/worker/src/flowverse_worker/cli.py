from __future__ import annotations

import argparse
import asyncio
from collections.abc import Sequence

import structlog

from flowverse_worker.core.logging import configure_logging
from flowverse_worker.core.settings import Settings
from flowverse_worker.core.telemetry import configure_telemetry
from flowverse_worker.health.postgres import PostgresProbe
from flowverse_worker.health.protocols import DependencyProbe

EXIT_OK = 0
EXIT_CONFIGURATION = 2
EXIT_DEPENDENCY = 3
EXIT_INTERRUPTED = 130

_LOGGER = structlog.get_logger("flowverse_worker.worker")


async def check_dependencies(
    settings: Settings,
    *,
    postgres_probe: DependencyProbe | None = None,
) -> int:
    probe = postgres_probe or PostgresProbe(settings)
    try:
        result = await probe.check()
        if result.status == "ready":
            _LOGGER.info("worker_check_succeeded", dependency="postgres")
            return EXIT_OK
        if result.reason == "configuration":
            _LOGGER.error("worker_check_failed", reason="configuration")
            return EXIT_CONFIGURATION
        _LOGGER.error("worker_check_failed", reason="dependency_unavailable")
        return EXIT_DEPENDENCY
    finally:
        await probe.close()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FlowVerse non-business worker bootstrap")
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate configuration and bounded PostgreSQL connectivity, then exit",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if not args.check:
        parser.error("only --check is available in the architecture bootstrap")

    settings = Settings()
    configure_logging(level=settings.log_level)
    configure_telemetry(service_name="flowverse-worker")
    try:
        return asyncio.run(check_dependencies(settings))
    except KeyboardInterrupt:
        _LOGGER.warning("worker_check_interrupted")
        return EXIT_INTERRUPTED
