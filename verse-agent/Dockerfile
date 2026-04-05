FROM python:3.11-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN python -m pip install --upgrade pip build

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m build --wheel

FROM python:3.11-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     PIP_DISABLE_PIP_VERSION_CHECK=1     APP_HOST=0.0.0.0     APP_PORT=8000

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /build/dist/*.whl /tmp/dist/

RUN python -m pip install --upgrade pip     && python -m pip install /tmp/dist/*.whl     && rm -rf /tmp/dist

RUN mkdir -p /app/logs && chown -R app:app /app

USER app

EXPOSE 8000

CMD ["uvicorn", "verse_agent.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
