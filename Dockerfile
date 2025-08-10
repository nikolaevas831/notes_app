FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .


RUN pip install uv
RUN uv sync

ENV PATH="/app/.venv/bin:$PATH"

CMD ["sh", "-c", "alembic upgrade head && uv run notes_app"]
