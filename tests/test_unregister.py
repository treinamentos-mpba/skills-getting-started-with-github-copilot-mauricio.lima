import unittest
from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app


class UnregisterTests(unittest.TestCase):
    def setUp(self):
        self.original_activities = deepcopy(activities)
        self.client = TestClient(app)

    def tearDown(self):
        activities.clear()
        activities.update(self.original_activities)
        self.client.close()

    def test_unregister_removes_only_the_selected_participant(self):
        response = self.client.delete(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            activities["Chess Club"]["participants"], ["daniel@mergington.edu"]
        )

    def test_unregister_unknown_participant_returns_404(self):
        response = self.client.delete(
            "/activities/Chess%20Club/signup", params={"email": "unknown@example.com"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(activities, self.original_activities)

    def test_unregister_unknown_activity_returns_404(self):
        response = self.client.delete(
            "/activities/Unknown/signup", params={"email": "michael@mergington.edu"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(activities, self.original_activities)


if __name__ == "__main__":
    unittest.main()