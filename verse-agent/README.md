# Verse Agent

`verse-agent` is a production-oriented Python backend skeleton built for future business modules. It provides a clean FastAPI foundation with typed configuration, async MySQL access, Redis encapsulation, Celery task wiring, structured logging, health endpoints, and isolated tests.

## Project Structure

```text
verse-agent/
|-- .env.example
|-- Dockerfile
|-- pyproject.toml
|-- README.md
|-- src/
|   `-- verse_agent/
|       |-- api/
|       |-- cache/
|       |-- core/
|       |-- db/
|       |-- schemas/
|       `-- tasks/
`-- tests/
```

## What This Skeleton Provides

- FastAPI application factory with liveness and readiness endpoints
- Versioned REST API router registration
- Centralized settings via environment variables only
- Async SQLAlchemy MySQL session management for future DAO/ORM work
- Redis adapter with `get`, `set`, `delete`, and `ping`
- Celery application factory and a minimal background task
- Unified Loguru logging for console and file sinks
- Global exception handlers and request ID middleware
- Pytest-based tests that do not require live MySQL or Redis instances

## Quick Start

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies:

```bash
pip install -e .[dev]
```

3. Copy the environment template and adjust values:

```bash
cp .env.example .env
```

4. Run the API server:

```bash
uvicorn verse_agent.main:create_app --factory --host 0.0.0.0 --port 8000 --reload
```

## Runtime Endpoints

- `GET /health` and `GET /api/v1/health`: process liveness only
- `GET /ready` and `GET /api/v1/ready`: dependency readiness for MySQL and Redis

## Environment Variables

All sensitive and deploy-time configuration is loaded in `src/verse_agent/core/config.py`.

- `APP_*`: application identity, runtime mode, host, port, reload, timezone
- `DATABASE__*`: async MySQL connection and SQLAlchemy pool configuration
- `REDIS__*`: Redis connectivity and client behavior
- `CELERY__*`: broker/backend URLs and worker execution settings
- `LOGGING__*`: log level, file path, rotation, retention, and serialization mode

### Production Safety Guardrails

When `APP_ENV=production`, the application now refuses to start if any of the following are still using local or placeholder defaults:

- `DATABASE__PASSWORD=change_me`
- `DATABASE__HOST` points to `localhost` / `127.0.0.1`
- `REDIS__HOST` points to `localhost` / `127.0.0.1`
- `CELERY__BROKER_URL` or `CELERY__RESULT_BACKEND` point to a local Redis address

This prevents accidental deployment with development placeholders.

## Running Tests

```bash
pytest
```

The tests validate:

- settings parsing and production-safety validation
- health and readiness responses
- Redis adapter behavior using mocks
- Celery factory and sample task behavior without real infrastructure

## Starting Celery

Start a worker:

```bash
celery -A verse_agent.tasks.celery_app.celery_app worker --loglevel=INFO
```

Trigger the example task from Python:

```python
from verse_agent.tasks.sample import emit_heartbeat

result = emit_heartbeat.delay("bootstrap")
```

## Extension Guidance

- Add ORM models under `src/verse_agent/db/models/`
- Add repositories or DAO modules under `src/verse_agent/db/repositories/`
- Add new API routers under `src/verse_agent/api/v1/endpoints/`
- Add background task modules under `src/verse_agent/tasks/`
- Keep infrastructure access inside adapters and avoid reading environment variables outside `core/config.py`
