from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class LivenessResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["alive"] = "alive"


class ReadinessResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ready", "unavailable"]


class PostgresDependencyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ready", "unavailable"]


class ObjectStorageDependencyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["deferred", "ready", "unavailable"]


class Dependencies(BaseModel):
    model_config = ConfigDict(extra="forbid")

    postgres: PostgresDependencyResponse
    object_storage: ObjectStorageDependencyResponse


class DependenciesResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ready", "degraded"]
    dependencies: Dependencies
