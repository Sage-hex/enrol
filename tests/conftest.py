import pytest
from fastapi.testclient import TestClient

from app.core.store import store
from app.main import app


@pytest.fixture(autouse=True)
def reset_store() -> None:
    store.reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
