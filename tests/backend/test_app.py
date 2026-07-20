from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_names = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == expected_activity_names

    for activity_name in expected_activity_names:
        assert "description" in payload[activity_name]
        assert "schedule" in payload[activity_name]
        assert "max_participants" in payload[activity_name]
        assert "participants" in payload[activity_name]


def test_signup_adds_participant_for_existing_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    existing_participants = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert len(activities[activity_name]["participants"]) == existing_participants + 1
    assert activities[activity_name]["participants"][-1] == email


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}