"""Base API response schemas."""

from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

PayloadT = TypeVar("PayloadT")


class ResponseMeta(BaseModel):
    """Response metadata for observability and tracing."""

    model_config = ConfigDict(extra="forbid")

    request_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ResponseEnvelope(BaseModel, Generic[PayloadT]):
    """Standard success response envelope."""

    model_config = ConfigDict(extra="forbid")

    success: bool = True
    data: PayloadT
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class ErrorDetail(BaseModel):
    """Error payload."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    details: dict[str, Any] | list[Any] | None = None


class ErrorEnvelope(BaseModel):
    """Standard error response envelope."""

    model_config = ConfigDict(extra="forbid")

    success: bool = False
    error: ErrorDetail
    meta: ResponseMeta = Field(default_factory=ResponseMeta)
