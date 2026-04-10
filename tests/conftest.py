import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activity state before and after each test."""
    original_state = copy.deepcopy(app_module.activities)

    # Reset state before test to ensure a clean baseline
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_state))

    yield

    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_state))


@pytest.fixture
def client():
    """Provide a reusable FastAPI test client."""
    return TestClient(app_module.app)
