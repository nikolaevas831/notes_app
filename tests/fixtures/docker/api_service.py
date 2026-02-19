import httpx
import pytest
from fastapi import status
from pytest_docker.plugin import Services


def is_responsive(base_url: str) -> bool:
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{base_url}/health")
            return response.status_code == status.HTTP_200_OK
    except httpx.HTTPError:
        return False


@pytest.fixture(scope="session")
def docker_api_service(docker_ip: str, docker_services: Services) -> str:
    port = docker_services.port_for("notes-app", 8000)
    base_url = f"http://{docker_ip}:{port}"

    # Ждём, пока сервис станет доступен
    docker_services.wait_until_responsive(
        timeout=60.0, pause=0.5, check=lambda: is_responsive(base_url=base_url)
    )
    return base_url
