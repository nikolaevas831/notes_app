import pytest


@pytest.fixture(scope="session")
def docker_compose_file() -> str:
    return "tests/api/docker-compose.api-tests.yml"
