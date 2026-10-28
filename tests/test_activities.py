from copy import deepcopy


def test_root_redirects_to_static_page(client):
    path = "/"

    response = client.get(path, follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_data(client, activity_data):
    expected_activities = deepcopy(activity_data)

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == expected_activities


def test_signup_adds_participant_to_activity(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": email})
    activities_response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities_response.json()["Chess Club"]["participants"]


def test_signup_rejects_duplicate_without_changing_activities(client, activity_data):
    email = "michael@mergington.edu"
    original_activities = deepcopy(activity_data)

    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activity_data == original_activities


def test_signup_rejects_unknown_activity_without_changing_activities(client, activity_data):
    original_activities = deepcopy(activity_data)

    response = client.post("/activities/Unknown/signup", params={"email": "new@example.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
    assert activity_data == original_activities


def test_signup_requires_email_without_changing_activities(client, activity_data):
    original_activities = deepcopy(activity_data)

    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422
    assert activity_data == original_activities