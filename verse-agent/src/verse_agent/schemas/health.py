"""Health check schemas."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthPayload(BaseModel):
    """Response model for liveness checks."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]
    service: str
    version: str
    environment: str


class DependencyHealth(BaseModel):
    """Per-dependency readiness result."""

    model_config = ConfigDict(extra="forbid")

    name: Literal["database", "redis"]
    status: Literal["ok", "error"]
    detail: str | None = None


class ReadinessPayload(BaseModel):
    """Response model for readiness checks."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ready", "degraded"]
    service: str
    version: str
    environment: str
    checks: list[DependencyHealth]
