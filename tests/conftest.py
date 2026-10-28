import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def activity_data(monkeypatch):
    activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        }
    }
    monkeypatch.setattr(app_module, "activities", activities)
    return activities


@pytest.fixture
def client(activity_data):
    with TestClient(app_module.app) as test_client:
        yield test_client