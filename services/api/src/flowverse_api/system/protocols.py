from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True, slots=True)
class WorkerProbeResult:
    status: Literal["ready", "unavailable"]
    reason: Literal[
        "ready",
        "configuration",
        "timeout",
        "probe_failure",
        "connection",
        "invalid_response",
    ]


class WorkerClient(Protocol):
    async def ping(self, *, request_id: str) -> WorkerProbeResult: ...

    async def close(self) -> None: ...
