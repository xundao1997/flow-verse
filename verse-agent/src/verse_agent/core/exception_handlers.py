"""Global exception handlers."""

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from verse_agent.core.errors import AppError
from verse_agent.schemas.common import ErrorDetail, ErrorEnvelope, ResponseMeta


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def _error_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any] | list[Any] | None = None,
) -> JSONResponse:
    payload = ErrorEnvelope(
        error=ErrorDetail(code=code, message=message, details=details),
        meta=ResponseMeta(request_id=_request_id(request)),
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump(mode="json"))


def register_exception_handlers(app: FastAPI) -> None:
    """Register shared exception handlers."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.bind(request_id=_request_id(request), component="error").warning(
            "Application error {}: {}", exc.code, exc.message
        )
        return _error_response(
            request,
            status_code=exc.status_code,
            code=exc.code,
            message=exc.message,
            details=exc.details,
        )

    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
        logger.bind(request_id=_request_id(request), component="error").warning(
            "HTTP error {} on {}", exc.status_code, request.url.path
        )
        return _error_response(
            request,
            status_code=exc.status_code,
            code="http_error",
            message=str(exc.detail),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return _error_response(
            request,
            status_code=422,
            code="validation_error",
            message="Request validation failed.",
            details=exc.errors(),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.bind(request_id=_request_id(request), component="error").exception(
            "Unhandled server error on {}", request.url.path
        )
        return _error_response(
            request,
            status_code=500,
            code="internal_server_error",
            message="An unexpected error occurred.",
        )
