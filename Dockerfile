FROM python:3.13-slim AS builder

ENV UV_VERSION="0.6.14"

WORKDIR /app

RUN pip install --no-cache-dir "uv==$UV_VERSION"

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-install-project

COPY src/ ./src/
COPY alembic.ini .

RUN uv sync --no-editable

ENV PATH="/app/.venv/bin:$PATH"

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ ./src/
COPY alembic.ini .
