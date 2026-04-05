"""Application middleware registration."""

from time import perf_counter
from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

RequestHandler = Callable[[Request], Awaitable[Response]]


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach a request ID and emit basic request lifecycle logs."""

    async def dispatch(self, request: Request, call_next: RequestHandler) -> Response:
        request_id = request.headers.get("X-Request-ID", uuid4().hex)
        request.state.request_id = request_id
        bound_logger = logger.bind(request_id=request_id, component="http")
        started_at = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            bound_logger.exception(
                "Request failed {} {}", request.method, request.url.path
            )
            raise

        elapsed_ms = (perf_counter() - started_at) * 1000
        response.headers["X-Request-ID"] = request_id
        bound_logger.info(
            "Request completed {} {} -> {} ({:.2f} ms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response


def register_middleware(app: FastAPI) -> None:
    """Register application middleware."""
    app.add_middleware(RequestContextMiddleware)
