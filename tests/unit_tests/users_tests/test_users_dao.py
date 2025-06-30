# THIRDPARTY
import pytest

# FIRSTPARTY
from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "user_id,email,exists",
    [
        (1, "user@example.com", True),
        (2, "step3210shelpyakov@gmail.com", True),
        (100, "not@exists.com", False),
    ],
)
async def test_find_by_id(user_id, email, exists):
    user = await UserDAO.find_by_id(user_id)

    if exists:
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user


# pyright: reportOptionalMemberAccess=false
