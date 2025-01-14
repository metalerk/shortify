import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.data.database import get_db


@pytest.fixture(autouse=True)
def mock_get_db():
    """
    Automatically mock the database session for all tests.
    """
    app.dependency_overrides[get_db] = lambda: MagicMock()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """
    Provide a test client for making API requests.
    """
    return TestClient(app)
