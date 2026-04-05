"""Celery application factory.

The module-level ``celery_app`` is kept for worker autodiscovery and task decoration.
Tests and alternate process entrypoints should prefer ``create_celery_app(settings)``
when they need explicit configuration instead of the cached application settings.
"""

from celery import Celery

from verse_agent.core.config import AppSettings, get_settings

CELERY_IMPORTS = ("verse_agent.tasks.sample",)


def create_celery_app(settings: AppSettings | None = None) -> Celery:
    """Create a Celery application from validated settings."""
    runtime_settings = settings or get_settings()
    application = Celery(
        "verse_agent",
        broker=runtime_settings.celery.broker_url,
        backend=runtime_settings.celery.result_backend,
        include=list(CELERY_IMPORTS),
    )
    application.conf.update(
        task_default_queue=runtime_settings.celery.task_default_queue,
        task_track_started=runtime_settings.celery.task_track_started,
        task_time_limit=runtime_settings.celery.task_time_limit,
        task_soft_time_limit=runtime_settings.celery.task_soft_time_limit,
        result_expires=runtime_settings.celery.result_expires,
        task_always_eager=runtime_settings.celery.task_always_eager,
        timezone=runtime_settings.timezone,
        enable_utc=True,
    )
    return application


celery_app = create_celery_app()
