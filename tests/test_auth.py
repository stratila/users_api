def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={
            "first_name": "John",
            "middle_name": "Doe",
            "last_name": "Smith",
            "email": "example@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"]

    response = client.get("/users/?email=example@test.com")
    assert response.status_code == 200
    assert response.json()[0]["id"]

    response = client.delete(f"/users/{response.json()[0]['id']}")
    assert response.status_code == 204


def test_login(client):
    response = client.post(
        "/auth/signup",
        json={
            "first_name": "John",
            "middle_name": "Doe",
            "last_name": "Smith",
            "email": "login@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"]

    response = client.post(
        "/auth/login",
        json={
            "email": "login@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"]

    response = client.get("/users/?email=login@test.com")
    assert response.status_code == 200
    assert response.json()[0]["id"]

    response = client.delete(f"/users/{response.json()[0]['id']}")
    assert response.status_code == 204
