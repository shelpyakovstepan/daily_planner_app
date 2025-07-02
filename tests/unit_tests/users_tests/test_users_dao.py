# THIRDPARTY
import pytest

# FIRSTPARTY
from app.users.dao import UserDAO


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "get_session", "mock_session", "create_users", "create_entries"
)
class TestUsersDAO:
    @pytest.mark.parametrize(
        "user_id,email,exists",
        [
            (1, "user@example.com", True),
            (2, "test@test.com", True),
            (100, "not@exists.com", False),
        ],
    )
    async def test_find_by_id(self, user_id, email, exists):
        user = await UserDAO.find_by_id(user_id)

        if exists:
            assert user.id == user_id
            assert user.email == email
        else:
            assert not user


# pyright: reportOptionalMemberAccess=false
