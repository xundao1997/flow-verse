from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class WorkerStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    service: Literal["flowverse-worker"]
    status: Literal["ready", "unavailable"]
    reason: Literal["ready", "configuration", "timeout", "probe_failure"]


class ServiceState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["ready", "unavailable"]
    reason: Literal[
        "ready",
        "configuration",
        "timeout",
        "probe_failure",
        "connection",
        "invalid_response",
    ]


class ChainServices(BaseModel):
    model_config = ConfigDict(extra="forbid")
    api: ServiceState
    worker: ServiceState


class ChainResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["ready", "degraded"]
    services: ChainServices
