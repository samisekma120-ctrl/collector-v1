from dataclasses import dataclass

import pytest
from fastapi import HTTPException

from app.api.deps import require_admin
from app.models.user import UserRole


@dataclass
class DummyUser:
    role: str


def test_require_admin_allows_admin() -> None:
    user = DummyUser(role=UserRole.admin)
    assert require_admin(current_user=user) == user


@pytest.mark.parametrize("role", [UserRole.buyer, UserRole.seller])
def test_require_admin_denies_non_admin(role: str) -> None:
    user = DummyUser(role=role)
    with pytest.raises(HTTPException) as exc:
        require_admin(current_user=user)

    assert exc.value.status_code == 403
