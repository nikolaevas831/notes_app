from collections.abc import AsyncGenerator
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from notes_app.infrastructure.config import Config


@pytest.fixture
async def client_for_integration_test(
    app: FastAPI, config: Config
) -> AsyncGenerator[AsyncClient, Any]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url=f"http://{config.api.host}:{config.api.port}"
    ) as client:
        yield client


@pytest.fixture
async def client_for_api_test(docker_api_service: str) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(base_url=docker_api_service) as client:
        yield client
