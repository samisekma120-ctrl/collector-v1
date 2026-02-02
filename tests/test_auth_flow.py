import os
import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def _check_env():
    assert os.getenv("DATABASE_URL")
    assert os.getenv("JWT_SECRET")


@pytest.fixture()
def client():
    return TestClient(app)


def test_register_login_me_flow(client: TestClient):
    email = f"user_{uuid.uuid4().hex}@example.com"
    password = "StrongPassw0rd!"

    # register
    r = client.post(
        "/auth/register",
        json={"email": email, "password": password, "role": "seller"},
    )
    assert r.status_code == 201, r.text

    # login
    r = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    # /me
    r = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["email"] == email
    assert body["role"] == "seller"


def test_me_without_token(client: TestClient):
    r = client.get("/me")
    assert r.status_code in (401, 403)
