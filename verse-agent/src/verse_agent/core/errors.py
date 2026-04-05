"""Stable application exception types."""

from typing import Any


class AppError(Exception):
    """Base application error mapped to a consistent HTTP response."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


class InfrastructureError(AppError):
    """Error raised when external infrastructure is unavailable."""

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            code="infrastructure_error",
            message=message,
            status_code=503,
            details=details,
        )
