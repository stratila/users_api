import pytest
from secrets import token_hex
from pathlib import Path

from fastapi.testclient import TestClient

from users_db.users import create_user, delete_user
from users_db.role_permissions import ROLE_SUPER_ADMIN
from users_api.utils.read_permissions import read_permissions_from_csv
from users_api.security.password import get_password_hash
from users_api.app import app


@pytest.fixture(scope="module", autouse=True)
def load_permissions():
    """Load permissions from CSV file"""
    path = Path(__file__).parent.parent / "users_api/security/role_permissions.csv"
    read_permissions_from_csv(path)


@pytest.fixture(scope="module")
def super_admin_password():
    return "password123"


@pytest.fixture(scope="module")
def super_admin_bearer(super_admin_password):
    super_admin_id = create_user(
        first_name="Super",
        middle_name="Admin",
        last_name="Test",
        email="SuperAdminTest@test.com",
        password=get_password_hash(super_admin_password),
        role=ROLE_SUPER_ADMIN,
    )

    client = TestClient(app)
    response = client.post(
        "/auth/login",
        json={
            "email": "SuperAdminTest@test.com",
            "password": super_admin_password,
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"]

    yield response.json()["access_token"]

    delete_user(super_admin_id)


@pytest.fixture(scope="module")
def client(super_admin_bearer):
    return TestClient(app, headers={"Authorization": f"Bearer {super_admin_bearer}"})


@pytest.fixture(scope="function")
def users_data(client):
    data = {}
    users = {}
    for i in range(2):
        response = client.post(
            "/users/",
            json={
                "first_name": f"{token_hex(8)}",
                "middle_name": f"{token_hex(8)}",
                "last_name": f"{token_hex(8)}",
                "email": f"{token_hex(8)}@test.com",
                "password": f"{token_hex(8)}",
                "role": "USER",
            },
        )
        assert response.status_code == 201
        users[f"user_{i}"] = response.json()
    data["users"] = users

    yield data

    for user in data["users"].values():
        response = client.delete(f"/users/{user['id']}")
        assert response.status_code == 204
