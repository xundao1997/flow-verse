from __future__ import annotations

import logging
import sys

import structlog

_configured = False


def configure_logging(*, level: str = "INFO") -> None:
    global _configured
    if _configured:
        return

    resolved_level = logging.getLevelNamesMapping()[level]
    logging.basicConfig(stream=sys.stdout, format="%(message)s", level=resolved_level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(resolved_level),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )
    _configured = True
