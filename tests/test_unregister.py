from copy import deepcopy


def test_unregister_removes_only_the_selected_participant(client, activity_data):
    email = "michael@mergington.edu"

    response = client.delete("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert activity_data["Chess Club"]["participants"] == ["daniel@mergington.edu"]


def test_unregister_unknown_participant_returns_404(client, activity_data):
    original_activities = deepcopy(activity_data)

    response = client.delete(
        "/activities/Chess%20Club/signup", params={"email": "unknown@example.com"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"
    assert activity_data == original_activities


def test_unregister_unknown_activity_returns_404(client, activity_data):
    original_activities = deepcopy(activity_data)

    response = client.delete(
        "/activities/Unknown/signup", params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
    assert activity_data == original_activities


def test_signup_then_unregister_restores_participants(client, activity_data):
    email = "new.student@mergington.edu"
    original_participants = activity_data["Chess Club"]["participants"].copy()

    signup_response = client.post("/activities/Chess%20Club/signup", params={"email": email})
    unregister_response = client.delete("/activities/Chess%20Club/signup", params={"email": email})
    activities_response = client.get("/activities")

    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert activities_response.json()["Chess Club"]["participants"] == original_participants