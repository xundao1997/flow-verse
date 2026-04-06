"""Loguru configuration for API and worker processes."""

import logging
import sys
from pathlib import Path

from loguru import logger

from verse_agent.core.config import LoggingSettings

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "{extra[component]} | "
    "{extra[request_id]} | "
    "{message}"
)


class InterceptHandler(logging.Handler):
    """Forward standard library logs to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.bind(component=record.name, request_id="-").opt(
            depth=6,
            exception=record.exc_info,
        ).log(level, record.getMessage())


def _configure_stdlib_logging() -> None:
    intercept_handler = InterceptHandler()
    logging.basicConfig(handlers=[intercept_handler], level=0, force=True)

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "celery"):
        target_logger = logging.getLogger(logger_name)
        target_logger.handlers = [intercept_handler]
        target_logger.propagate = False


def _log_file_path(settings: LoggingSettings) -> Path:
    directory = Path(settings.directory).expanduser()
    if not directory.is_absolute():
        directory = Path.cwd() / directory
    directory.mkdir(parents=True, exist_ok=True)
    return directory / settings.file_name


def configure_logging(settings: LoggingSettings) -> None:
    """Configure Loguru sinks and intercept stdlib logging."""
    logger.remove()
    logger.configure(extra={"component": "app", "request_id": "-"})

    logger.add(
        sys.stdout,
        level=settings.level.upper(),
        format=LOG_FORMAT,
        backtrace=False,
        diagnose=False,
        enqueue=True,
        serialize=settings.serialize,
    )
    logger.add(
        _log_file_path(settings),
        level=settings.level.upper(),
        format=LOG_FORMAT,
        rotation=settings.rotation,
        retention=settings.retention,
        compression=settings.compression,
        backtrace=False,
        diagnose=False,
        enqueue=True,
        serialize=settings.serialize,
    )

    _configure_stdlib_logging()
