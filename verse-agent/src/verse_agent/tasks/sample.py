"""Minimal Celery task used to verify worker wiring."""

from datetime import datetime, timezone

from verse_agent.tasks.celery_app import celery_app


@celery_app.task(name="verse_agent.tasks.emit_heartbeat")
def emit_heartbeat(job_name: str = "bootstrap") -> dict[str, str]:
    """Return a lightweight payload to validate task execution."""
    return {
        "job": job_name,
        "status": "accepted",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
