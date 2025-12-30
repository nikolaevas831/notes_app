FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-install-project

COPY src/ ./src/
COPY alembic.ini .

RUN uv sync --no-editable

ENV PATH="/app/.venv/bin:$PATH"
