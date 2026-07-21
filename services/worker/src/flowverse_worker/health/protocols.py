from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True, slots=True)
class ProbeResult:
    status: Literal["ready", "unavailable"]
    reason: Literal["ready", "configuration", "timeout", "probe_failure"]


class DependencyProbe(Protocol):
    async def check(self) -> ProbeResult: ...

    async def close(self) -> None: ...
