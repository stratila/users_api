from users_db.role_permissions import (
    ROLE_USER,
)
from users_api.schemas.users import (
    UserRead,
)

from pydantic import parse_obj_as


def test_get_users(client, users_data):
    response = client.get("/users/", params={"role": ROLE_USER})
    assert response.status_code == 200

    users = parse_obj_as(list[UserRead], response.json())

    for user in users:
        for user_data in users_data["users"].values():
            if user.id == user_data["id"]:
                assert user.first_name == user_data["first_name"]
                assert user.middle_name == user_data["middle_name"]
                assert user.last_name == user_data["last_name"]
                assert user.email == user_data["email"]
                assert user.role == user_data["role"]


def test_get_user(client, users_data):
    user = users_data["users"]["user_0"]
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200

    response_user = parse_obj_as(UserRead, response.json())
    assert response_user.id == user["id"]
    assert response_user.first_name == user["first_name"]
    assert response_user.middle_name == user["middle_name"]
    assert response_user.last_name == user["last_name"]
    assert response_user.email == user["email"]
    assert response_user.role == user["role"]


def test_post_user(client):
    response = client.post(
        "/users/",
        json={
            "first_name": "John",
            "middle_name": "Doe",
            "last_name": "Smith",
            "email": "example1@test.com",
            "password": "password123",
            "role": ROLE_USER,
        },
    )

    assert response.status_code == 201

    response_user = parse_obj_as(UserRead, response.json())
    assert response_user.id
    assert response_user.first_name == "John"
    assert response_user.middle_name == "Doe"
    assert response_user.last_name == "Smith"
    assert response_user.email == "example1@test.com"
    assert response_user.role == ROLE_USER

    # clean up
    response = client.delete(f"/users/{response.json()['id']}")
    assert response.status_code == 204


def test_put_user(client, users_data):
    user = users_data["users"]["user_0"]
    response = client.put(
        f"/users/{user['id']}",
        json={
            "first_name": "John2",
            "middle_name": "Doe2",
            "last_name": "Smith2",
        },
    )
    assert response.status_code == 200

    response_user = parse_obj_as(UserRead, response.json())

    # unchanged fields
    assert response_user.id == user["id"]
    assert response_user.email == user["email"]
    assert response_user.role == user["role"]
    # changed fields
    assert response_user.first_name == "John2"
    assert response_user.middle_name == "Doe2"
    assert response_user.last_name == "Smith2"


def test_delete_user(client):
    # create user
    response = client.post(
        "/users/",
        json={
            "first_name": "John",
            "middle_name": "Doe",
            "last_name": "Smith",
            "email": "example1@test.com",
            "password": "password123",
            "role": "USER",
        },
    )
    assert response.status_code == 201
    assert response.json()["id"]
    deleted_user_id = response.json()["id"]

    # delete user
    response = client.delete(f"/users/{response.json()['id']}")
    assert response.status_code == 204

    # check if user is deleted
    response = client.get(f"/users/{deleted_user_id}")
    assert response.status_code == 404


# bad requests


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404


def test_put_user_not_found(client, users_data):
    user_0 = users_data["users"]["user_0"]
    response = client.put("/users/999", json=user_0)
    assert response.status_code == 404
