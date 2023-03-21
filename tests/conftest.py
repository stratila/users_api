import pytest

from secrets import token_hex


@pytest.fixture(scope="module", autouse=True)
def client():
    from users_api.app import app
    from fastapi.testclient import TestClient

    return TestClient(app)


@pytest.fixture(scope="function")
def users_data(client):
    data = []
    users = {}
    for i in range(2):
        response = client.post(
            "/users/",
            json={
                "first_name": f"{token_hex(8)}",
                "middle_name": f"{token_hex(8)}",
                "last_name": f"{token_hex(8)}",
            },
        )
        assert response.status_code == 201
        users[f"user_{i}"] = response.json()
    data.append(users)

    yield data

    for d in data:
        for user in d.values():
            response = client.delete(f"/users/{user['id']}")
            assert response.status_code == 204
