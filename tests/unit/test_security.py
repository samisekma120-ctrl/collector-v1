import os

import pytest
from fastapi import HTTPException

os.environ.setdefault("JWT_SECRET", "unit_test_secret")
os.environ.setdefault("JWT_ALG", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "1")

from app.core.security import (  # noqa: E402
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_and_verify_password_ok() -> None:
    hashed = hash_password("Test1234!")
    assert isinstance(hashed, str)
    assert hashed != "Test1234!"
    assert verify_password("Test1234!", hashed) is True


def test_verify_password_wrong_password() -> None:
    hashed = hash_password("Test1234!")
    assert verify_password("WrongPassword!", hashed) is False


def test_verify_password_invalid_hash_returns_false() -> None:
    assert verify_password("Test1234!", "not-a-valid-bcrypt-hash") is False


def test_create_and_decode_token_roundtrip() -> None:
    token = create_access_token(
        "11111111-1111-1111-1111-111111111111",
        extra_claims={"role": "buyer"},
    )
    payload = decode_token(token)

    assert payload["sub"] == "11111111-1111-1111-1111-111111111111"
    assert payload["role"] == "buyer"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_token_invalid_raises_401() -> None:
    with pytest.raises(HTTPException) as exc:
        decode_token("this.is.not.valid")

    assert exc.value.status_code == 401


def test_token_has_exp_greater_than_iat() -> None:
    token = create_access_token("sub")
    payload = decode_token(token)
    assert payload["exp"] > payload["iat"]
