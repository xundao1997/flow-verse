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
    redis_host: str = "127.0.0.1"
    redis_port: int = Field(default=16379, ge=1, le=65535)
    redis_password: SecretStr | None = None
    minio_endpoint: AnyHttpUrl | None = None
    minio_access_key: SecretStr | None = None
    minio_secret_key: SecretStr | None = None
    minio_region: str = Field(default="us-east-1", min_length=1, max_length=64)
    middleware_probe_timeout_seconds: float = Field(default=3.0, gt=0.0, le=10.0)
    worker_base_url: AnyHttpUrl = AnyHttpUrl("http://127.0.0.1:8001")
    worker_request_timeout_seconds: float = Field(default=2.0, gt=0.0, le=10.0)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
