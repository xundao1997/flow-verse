"""Centralized application settings."""

from functools import lru_cache
from pathlib import Path
from urllib.parse import quote, urlsplit

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parents[3]
DEFAULT_PLACEHOLDER_PASSWORD = "change_me"
LOCAL_HOSTS = {"127.0.0.1", "localhost", "0.0.0.0", "::1"}


class LoggingSettings(BaseModel):
    """Logging configuration."""

    level: str = "INFO"
    directory: Path = BASE_DIR / "logs"
    file_name: str = "verse-agent.log"
    rotation: str = "10 MB"
    retention: str = "14 days"
    compression: str = "zip"
    serialize: bool = False


class DatabaseSettings(BaseModel):
    """Async MySQL configuration."""

    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "verse_agent"
    password: SecretStr = SecretStr(DEFAULT_PLACEHOLDER_PASSWORD)
    name: str = "verse_agent"
    echo: bool = False
    pool_pre_ping: bool = True
    pool_recycle: int = 1800
    pool_size: int = 10
    max_overflow: int = 10
    connect_timeout: int = 10

    @property
    def sqlalchemy_url(self) -> str:
        """Build the SQLAlchemy async connection URL."""
        return URL.create(
            drivername="mysql+aiomysql",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
            query={"charset": "utf8mb4"},
        ).render_as_string(hide_password=False)

    @property
    def uses_placeholder_password(self) -> bool:
        """Return whether the configured password is still the placeholder value."""
        return self.password.get_secret_value() == DEFAULT_PLACEHOLDER_PASSWORD


class RedisSettings(BaseModel):
    """Redis connectivity settings."""

    host: str = "127.0.0.1"
    port: int = 6379
    db: int = 0
    username: str | None = None
    password: SecretStr | None = None
    decode_responses: bool = True
    socket_timeout: float = 5.0
    health_check_interval: int = 30

    @property
    def url(self) -> str:
        """Build the Redis URL."""
        username = quote(self.username) if self.username else ""
        password = (
            quote(self.password.get_secret_value())
            if self.password and self.password.get_secret_value()
            else ""
        )
        if username and password:
            credentials = f"{username}:{password}@"
        elif password:
            credentials = f":{password}@"
        else:
            credentials = ""
        return f"redis://{credentials}{self.host}:{self.port}/{self.db}"


class CelerySettings(BaseModel):
    """Celery worker configuration."""

    broker_url: str = "redis://127.0.0.1:6379/1"
    result_backend: str = "redis://127.0.0.1:6379/2"
    task_default_queue: str = "verse-agent.default"
    task_track_started: bool = True
    task_time_limit: int = 300
    task_soft_time_limit: int = 240
    result_expires: int = 3600
    task_always_eager: bool = False


class AppSettings(BaseSettings):
    """Root application settings loaded from environment variables."""

    app_name: str = "Verse Agent"
    app_env: str = "local"
    app_version: str = "0.1.0"
    host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    port: int = Field(default=8000, validation_alias="APP_PORT")
    reload: bool = Field(default=False, validation_alias="APP_RELOAD")
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    timezone: str = Field(default="UTC", validation_alias="APP_TIMEZONE")
    api_v1_prefix: str = "/api/v1"
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    celery: CelerySettings = Field(default_factory=CelerySettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=False,
        populate_by_name=True,
    )

    def model_post_init(self, __context: object) -> None:
        """Reject unsafe fallbacks in production-like environments."""
        self.validate_runtime_safety()

    @property
    def is_production(self) -> bool:
        """Return whether the application is running in a production-like mode."""
        return self.app_env.strip().lower() == "production"

    def validate_runtime_safety(self) -> None:
        """Prevent accidental production startup with placeholder or local defaults."""
        if not self.is_production:
            return

        errors: list[str] = []
        if self.database.uses_placeholder_password:
            errors.append("DATABASE__PASSWORD must not use the default placeholder in production.")
        if self.database.host.strip().lower() in LOCAL_HOSTS:
            errors.append("DATABASE__HOST must not point to a local address in production.")
        if self.redis.host.strip().lower() in LOCAL_HOSTS:
            errors.append("REDIS__HOST must not point to a local address in production.")

        for field_name, url in {
            "CELERY__BROKER_URL": self.celery.broker_url,
            "CELERY__RESULT_BACKEND": self.celery.result_backend,
        }.items():
            parsed = urlsplit(url)
            if parsed.hostname and parsed.hostname.strip().lower() in LOCAL_HOSTS:
                errors.append(f"{field_name} must not point to a local address in production.")

        if errors:
            raise ValueError(" ".join(errors))


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Return cached application settings."""
    return AppSettings()


def reset_settings_cache() -> None:
    """Clear the cached settings for tests."""
    get_settings.cache_clear()
