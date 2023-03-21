import pytest


def test_get_users(client, users_data):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2

    for user in response.json():
        assert user["id"] in [
            users_data[0]["user_0"]["id"],
            users_data[0]["user_1"]["id"],
        ]
        assert user["first_name"] in [
            users_data[0]["user_0"]["first_name"],
            users_data[0]["user_1"]["first_name"],
        ]
        assert user["middle_name"] in [
            users_data[0]["user_0"]["middle_name"],
            users_data[0]["user_1"]["middle_name"],
        ]
        assert user["last_name"] in [
            users_data[0]["user_0"]["last_name"],
            users_data[0]["user_1"]["last_name"],
        ]


def test_post_user(client):
    response = client.post(
        "/users/",
        json={
            "first_name": "John",
            "middle_name": "Doe",
            "last_name": "Smith",
        },
    )
    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["first_name"] == "John"
    assert response.json()["middle_name"] == "Doe"
    assert response.json()["last_name"] == "Smith"

    # clean up
    response = client.delete(f"/users/{response.json()['id']}")
    assert response.status_code == 204
