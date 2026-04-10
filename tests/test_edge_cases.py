import src.app as app_module


def test_signup_allows_empty_email_current_behavior(client):
    # Arrange
    activity_name = "Chess Club"
    empty_email = ""
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": empty_email})

    # Assert
    assert response.status_code == 200
    assert empty_email in app_module.activities[activity_name]["participants"]


def test_signup_activity_name_is_case_sensitive(client):
    # Arrange
    activity_name = "chess club"
    email = "case.check@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_capacity_boundary_last_spot_then_full(client):
    # Arrange
    activity_name = "Chess Club"
    path = f"/activities/{activity_name}/signup"
    max_participants = app_module.activities[activity_name]["max_participants"]
    app_module.activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants - 1)
    ]
    last_spot_email = "last.spot@mergington.edu"
    overflow_email = "overflow@mergington.edu"

    # Act
    last_spot_response = client.post(path, params={"email": last_spot_email})
    overflow_response = client.post(path, params={"email": overflow_email})

    # Assert
    assert last_spot_response.status_code == 200
    assert overflow_response.status_code == 400
    assert overflow_response.json()["detail"] == "Activity is full"
    assert last_spot_email in app_module.activities[activity_name]["participants"]
    assert overflow_email not in app_module.activities[activity_name]["participants"]
