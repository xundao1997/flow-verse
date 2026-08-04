FROM ghcr.nju.edu.cn/astral-sh/uv:0.11.28 AS uv
FROM docker.nju.edu.cn/python:3.13.14-slim-bookworm

COPY --from=uv /uv /uvx /usr/local/bin/

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONPATH=/app/src \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_FROZEN=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1

RUN addgroup --system flowverse \
    && adduser --system --ingroup flowverse --home /app flowverse

WORKDIR /app

COPY services/worker/pyproject.toml services/worker/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY services/worker/ ./
RUN uv sync --frozen --no-dev \
    && chown -R flowverse:flowverse /app

USER flowverse

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8001/health/live', timeout=2)"]

CMD ["python", "-m", "uvicorn", "flowverse_worker.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
