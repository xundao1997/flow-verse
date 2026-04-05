"""Celery tasks package."""

from verse_agent.tasks.celery_app import celery_app

__all__ = ["celery_app"]
