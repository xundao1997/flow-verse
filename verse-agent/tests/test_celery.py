"""Tests for Celery wiring."""

from verse_agent.core.config import AppSettings, CelerySettings
from verse_agent.tasks.celery_app import create_celery_app
from verse_agent.tasks.sample import emit_heartbeat


def test_celery_factory_applies_settings() -> None:
    settings = AppSettings(
        celery=CelerySettings(
            broker_url="redis://127.0.0.1:6379/9",
            result_backend="redis://127.0.0.1:6379/10",
            task_default_queue="unit-test",
            task_always_eager=True,
        )
    )

    celery_app = create_celery_app(settings)

    assert celery_app.conf.broker_url == "redis://127.0.0.1:6379/9"
    assert celery_app.conf.result_backend == "redis://127.0.0.1:6379/10"
    assert celery_app.conf.task_default_queue == "unit-test"
    assert celery_app.conf.task_always_eager is True


def test_sample_task_returns_structured_payload() -> None:
    payload = emit_heartbeat.run("unit-test")

    assert payload["job"] == "unit-test"
    assert payload["status"] == "accepted"
    assert "timestamp" in payload
