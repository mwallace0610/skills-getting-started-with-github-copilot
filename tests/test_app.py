import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    response = client.post("/activities/Basketball Team/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "tester@mergington.edu" in response.json()["message"]

    # Clean up: remove participant
    client.delete("/activities/Basketball Team/participants/tester@mergington.edu")

def test_remove_participant():
    # Add participant first
    client.post("/activities/Drama Club/signup?email=remove@mergington.edu")
    response = client.delete("/activities/Drama Club/participants/remove@mergington.edu")
    assert response.status_code == 200
    assert "removed" in response.json()["message"]

    # Try removing again (should 404)
    response = client.delete("/activities/Drama Club/participants/remove@mergington.edu")
    assert response.status_code == 404

@pytest.mark.parametrize("activity", ["Chess Club", "Programming Class", "Gym Class"])
def test_activity_exists(activity):
    response = client.get("/activities")
    assert activity in response.json()
