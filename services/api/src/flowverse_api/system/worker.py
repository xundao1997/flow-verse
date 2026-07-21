from __future__ import annotations

import httpx
import structlog
from opentelemetry.propagate import inject

from flowverse_api.core.settings import Settings
from flowverse_api.system.models import WorkerStatusResponse
from flowverse_api.system.protocols import WorkerProbeResult

_LOGGER = structlog.get_logger("flowverse_api.system.worker")


class HttpxWorkerClient:
    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=str(settings.worker_base_url),
            timeout=httpx.Timeout(settings.worker_request_timeout_seconds),
            transport=transport,
        )

    async def ping(self, *, request_id: str) -> WorkerProbeResult:
        headers = {"x-request-id": request_id}
        inject(headers)
        try:
            response = await self._client.get("/internal/v1/system/status", headers=headers)
        except httpx.TimeoutException:
            _LOGGER.warning("worker_ping_unavailable", reason="timeout")
            return WorkerProbeResult(status="unavailable", reason="timeout")
        except httpx.RequestError as exc:
            _LOGGER.warning(
                "worker_ping_unavailable",
                reason="connection",
                error_type=type(exc).__name__,
            )
            return WorkerProbeResult(status="unavailable", reason="connection")

        if response.status_code not in (200, 503):
            _LOGGER.warning(
                "worker_ping_unavailable",
                reason="invalid_response",
                status_code=response.status_code,
            )
            return WorkerProbeResult(status="unavailable", reason="invalid_response")
        try:
            worker_status = WorkerStatusResponse.model_validate(response.json())
        except (TypeError, ValueError):
            _LOGGER.warning("worker_ping_unavailable", reason="invalid_response")
            return WorkerProbeResult(status="unavailable", reason="invalid_response")
        expected_status_code = 200 if worker_status.status == "ready" else 503
        if response.status_code != expected_status_code:
            _LOGGER.warning("worker_ping_unavailable", reason="invalid_response")
            return WorkerProbeResult(status="unavailable", reason="invalid_response")
        return WorkerProbeResult(status=worker_status.status, reason=worker_status.reason)

    async def close(self) -> None:
        await self._client.aclose()
