from __future__ import annotations

from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FLOWVERSE_",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: SecretStr | None = None
    postgres_probe_timeout_seconds: float = Field(default=2.0, gt=0.0, le=10.0)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
