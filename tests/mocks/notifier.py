from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def notifier_mock() -> AsyncMock:
    return AsyncMock()
