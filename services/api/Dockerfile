FROM crpi-gtjoy2et81jlceyo-vpc.cn-beijing.personal.cr.aliyuncs.com/zfq-common/uv:0.11.28 AS uv
FROM crpi-gtjoy2et81jlceyo-vpc.cn-beijing.personal.cr.aliyuncs.com/zfq-common/python:3.13.14-slim-bookworm

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

COPY services/api/pyproject.toml services/api/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY services/api/ ./
RUN uv sync --frozen --no-dev \
    && chown -R flowverse:flowverse /app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2)"]

USER flowverse

CMD ["python", "-m", "uvicorn", "flowverse_api.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
