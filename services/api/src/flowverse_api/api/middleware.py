from __future__ import annotations

import re
from uuid import uuid4

import structlog
from fastapi import Request, Response
from opentelemetry import trace
from opentelemetry.propagate import extract
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

_REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
_TRACER = trace.get_tracer("flowverse_api.api")
_LOGGER = structlog.get_logger("flowverse_api.http")


def _request_id(value: str | None) -> str:
    if value is not None and _REQUEST_ID_PATTERN.fullmatch(value):
        return value
    return str(uuid4())


async def unhandled_exception_response(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", _request_id(None))
    trace_id = getattr(request.state, "trace_id", "0" * 32)
    _LOGGER.error(
        "http_request_failed",
        method=request.method,
        path=request.url.path,
        error_type=type(exc).__name__,
        request_id=request_id,
        trace_id=trace_id,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers={"x-request-id": request_id, "x-trace-id": trace_id},
    )


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = _request_id(request.headers.get("x-request-id"))
        with _TRACER.start_as_current_span(
            "http.request", context=extract(request.headers)
        ) as span:
            trace_id = f"{span.get_span_context().trace_id:032x}"
            structlog.contextvars.clear_contextvars()
            structlog.contextvars.bind_contextvars(request_id=request_id, trace_id=trace_id)
            request.state.request_id = request_id
            request.state.trace_id = trace_id
            status_code = 500
            try:
                response = await call_next(request)
                status_code = response.status_code
                response.headers["x-request-id"] = request_id
                response.headers["x-trace-id"] = trace_id
                return response
            finally:
                _LOGGER.info(
                    "http_request_completed",
                    method=request.method,
                    path=request.url.path,
                    status_code=status_code,
                )
                structlog.contextvars.clear_contextvars()
