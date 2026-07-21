from __future__ import annotations

from typing import Literal

from pydantic import AnyHttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FLOWVERSE_",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: SecretStr | None = None
    postgres_probe_timeout_seconds: float = Field(default=2.0, gt=0.0, le=10.0)
    worker_base_url: AnyHttpUrl = AnyHttpUrl("http://127.0.0.1:8001")
    worker_request_timeout_seconds: float = Field(default=2.0, gt=0.0, le=10.0)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
