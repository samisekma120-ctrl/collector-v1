import pytest
from fastapi import HTTPException

from app.api.routes.auth import validate_register_role  # adapte le chemin
from app.models.user import UserRole


def test_register_policy_denies_admin() -> None:
    with pytest.raises(HTTPException) as exc:
        validate_register_role(UserRole.admin)
    assert exc.value.status_code == 403


@pytest.mark.parametrize("role", [UserRole.buyer, UserRole.seller])
def test_register_policy_allows_non_admin(role: str) -> None:
    validate_register_role(role)  # ne doit pas lever