import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

# S'assurer que les variables sont set avant import app
os.environ.setdefault("JWT_SECRET", "test_secret")
os.environ.setdefault("JWT_ALG", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
)

from app.core.security import hash_password  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.models.category import Category  # noqa: E402  (adapte si ton modèle s'appelle autrement)
from app.models.user import User, UserRole  # noqa: E402


@pytest.fixture()
def db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def cleanup_db(db: Session) -> None:
    """
    Nettoyage simple entre tests.
    On supprime d'abord les catégories puis les users.
    """
    db.execute(delete(Category))
    db.execute(delete(User))
    db.commit()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def register(client: TestClient, email: str, password: str, role: str) -> dict:
    r = client.post(
        "/auth/register",
        json={"email": email, "password": password, "role": role},
    )
    return {"status": r.status_code, "json": r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text}


def login(client: TestClient, email: str, password: str) -> str:
    r = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    assert token
    return token



def create_admin_in_db(db: Session, email: str, password: str) -> User:
    admin = User(
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.admin,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_register_buyer_then_login_then_me(client: TestClient) -> None:
    email = f"buyer_{uuid.uuid4().hex[:8]}@example.com"
    password = "Test1234!"

    reg = register(client, email=email, password=password, role="buyer")
    assert reg["status"] in (200, 201), reg

    token = login(client, email, password)

    me = client.get("/me", headers=auth_headers(token))
    assert me.status_code == 200, me.text
    assert me.json()["email"] == email
    assert me.json()["role"] == "buyer"


def test_public_register_denies_admin_role(client: TestClient) -> None:
    email = f"admin_try_{uuid.uuid4().hex[:8]}@example.com"
    password = "Test1234!"

    r = client.post(
        "/auth/register",
        json={"email": email, "password": password, "role": "admin"},
    )

    # Selon ton implémentation : 403 (recommandé) ou 422
    assert r.status_code in (403, 422), r.text


def test_categories_rbac_buyer_forbidden_admin_allowed(client: TestClient, db: Session) -> None:
    # Buyer
    buyer_email = f"buyer_{uuid.uuid4().hex[:8]}@example.com"
    password = "Test1234!"
    reg = register(client, email=buyer_email, password=password, role="buyer")
    assert reg["status"] in (200, 201), reg
    buyer_token = login(client, buyer_email, password)

    # Admin (créé en DB comme une action Ops)
    admin_email = f"admin_{uuid.uuid4().hex[:8]}@example.com"
    create_admin_in_db(db, admin_email, password)
    admin_token = login(client, admin_email, password)

    # Public list categories
    pub = client.get("/categories")
    assert pub.status_code == 200, pub.text
    assert isinstance(pub.json(), list)

    # Buyer cannot create category
    r_forbid = client.post(
        "/categories",
        json={"name": "Sacs"},
        headers=auth_headers(buyer_token),
    )
    assert r_forbid.status_code == 403, r_forbid.text

    # Admin can create category
    r_ok = client.post(
        "/categories",
        json={"name": "Sacs"},
        headers=auth_headers(admin_token),
    )
    assert r_ok.status_code in (200, 201), r_ok.text

    # Public list should contain it
    pub2 = client.get("/categories")
    assert pub2.status_code == 200, pub2.text
    names = [c["name"] for c in pub2.json()]
    assert "Sacs" in names
