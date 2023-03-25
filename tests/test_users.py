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


def test_get_user(client, users_data):
    response = client.get(f"/users/{users_data[0]['user_0']['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == users_data[0]["user_0"]["id"]
    assert response.json()["first_name"] == users_data[0]["user_0"]["first_name"]
    assert response.json()["middle_name"] == users_data[0]["user_0"]["middle_name"]
    assert response.json()["last_name"] == users_data[0]["user_0"]["last_name"]


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


def test_put_user(client, users_data):
    response = client.put(
        f"/users/{users_data[0]['user_0']['id']}",
        json={
            "first_name": "John",
            "middle_name": "Doe",
            "last_name": "Smith",
        },
    )
    assert response.status_code == 200
    assert response.json()["id"] == users_data[0]["user_0"]["id"]
    assert response.json()["first_name"] == "John"
    assert response.json()["middle_name"] == "Doe"
    assert response.json()["last_name"] == "Smith"


def test_delete_user(client):
    # create user
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
    user_0 = users_data[0]["user_0"]
    response = client.put("/users/999", json=user_0)
    assert response.status_code == 404
