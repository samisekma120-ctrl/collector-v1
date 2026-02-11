import os
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt

# On garde alg/expire en "module constants" (pas dangereux)
JWT_ALG = os.getenv("JWT_ALG", "HS256").strip()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def get_jwt_secret() -> str:
    """
    Récupère le secret JWT au runtime.
    IMPORTANT: ne jamais lever une erreur au moment de l'import du module.
    """
    secret = os.getenv("JWT_SECRET", "").strip()
    if not secret:
        raise RuntimeError("JWT_SECRET is not set")
    return secret


def hash_password(password: str) -> str:
    pw = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw, salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    pw = password.encode("utf-8")
    hpw = hashed_password.encode("utf-8")
    try:
        return bcrypt.checkpw(pw, hpw)
    except ValueError:
        return False


def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),  # plus standard JSON/JWT
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALG)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALG])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e
