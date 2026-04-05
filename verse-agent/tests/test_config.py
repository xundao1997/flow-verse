"""Configuration tests."""

import pytest

from verse_agent.core.config import get_settings


def test_settings_load_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "Verse Agent Test")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_TIMEZONE", "Asia/Shanghai")
    monkeypatch.setenv("DATABASE__HOST", "mysql.internal")
    monkeypatch.setenv("DATABASE__PORT", "3307")
    monkeypatch.setenv("DATABASE__PASSWORD", "secret")
    monkeypatch.setenv("REDIS__PORT", "6380")
    monkeypatch.setenv("CELERY__TASK_ALWAYS_EAGER", "true")

    settings = get_settings()

    assert settings.app_name == "Verse Agent Test"
    assert settings.app_env == "test"
    assert settings.timezone == "Asia/Shanghai"
    assert settings.database.host == "mysql.internal"
    assert settings.database.port == 3307
    assert settings.database.password.get_secret_value() == "secret"
    assert settings.database.sqlalchemy_url.startswith("mysql+aiomysql://")
    assert settings.redis.port == 6380
    assert settings.celery.task_always_eager is True


def test_production_settings_reject_placeholder_defaults(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")

    with pytest.raises(ValueError, match="DATABASE__PASSWORD"):
        get_settings()


def test_production_settings_require_non_local_services(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DATABASE__PASSWORD", "strong-secret")
    monkeypatch.setenv("DATABASE__HOST", "mysql.internal")
    monkeypatch.setenv("REDIS__HOST", "redis.internal")
    monkeypatch.setenv("CELERY__BROKER_URL", "redis://redis.internal:6379/1")
    monkeypatch.setenv("CELERY__RESULT_BACKEND", "redis://redis.internal:6379/2")

    settings = get_settings()

    assert settings.is_production is True
    assert settings.database.host == "mysql.internal"
