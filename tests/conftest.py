# STDLIB
from datetime import datetime
import json
from typing import AsyncGenerator, List

# THIRDPARTY
import httpx
from httpx import AsyncClient
import pytest
from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.database import async_session_maker
from app.entries.models import Entries
from app.main import app as fastapi_app
from app.users.models import Users

# @pytest.fixture(scope="session", autouse=True)
# async def prepare_database():
#   assert settings.MODE == "TEST"
#   async with engine.begin() as connection:
#       await connection.run_sync(Base.metadata.drop_all)
#       await connection.run_sync(Base.metadata.create_all)


def open_mock_json(model: str):
    with open(f"tests/mock_{model}.json", "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(scope="function")
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для создания экземпляра сессии базы данных для тестов.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy для проведения тестов.
    """
    test_session = async_session_maker
    async with test_session() as t_session:
        try:
            yield t_session
        finally:
            await t_session.rollback()


@pytest.fixture(scope="function", autouse=True)
async def create_users(
    get_session: AsyncSession,
) -> AsyncGenerator[List[Users], None]:
    """Фикстура для создания тестового пользователя в БД.

    Args:
        get_session (AsyncSession): Асинхронная сессия базы данных

    Returns:
        Users: Экземпляр модели Users, представляющий созданного
        пользователя
    """
    users = open_mock_json("users")
    users_list = []
    for user in users:
        user = Users(
            id=user["id"],
            email=user["email"],
            hashed_password=user["hashed_password"],
            is_admin=user["is_admin"],
        )
        users_list.append(user)

    get_session.add_all(users_list)
    await get_session.commit()

    yield users_list

    for user in users_list:
        query = delete(Entries).where(Entries.user_id == user.id)
        await get_session.execute(query)
        await get_session.commit()
        query = delete(Users).where(Users.id == user.id)
        await get_session.execute(query)
        await get_session.commit()


@pytest.fixture(scope="function", autouse=True)
async def create_entries(
    get_session: AsyncSession,
    create_users: List[Users],  # noqa: F811
) -> AsyncGenerator[List[Entries], None]:
    """Фикстура для создания тестовой активности в БД.

    Args:
       get_session: Асинхронная сессия базы данных
       create_users: Экземпляр модели UsersModel

    Returns:
       Entries: Экземпляр модели Entries, представляющий
       созданную активность
    """
    entries = open_mock_json("entries")
    entries_list = []
    for entry in entries:
        entry["date_start"] = datetime.strptime(entry["date_start"], "%Y-%m-%d")
        entry["date_end"] = datetime.strptime(entry["date_end"], "%Y-%m-%d")

        entry = Entries(
            id=entry["id"],
            user_id=entry["user_id"],
            date_start=entry["date_start"],
            date_end=entry["date_end"],
            text=entry["text"],
            status=entry["status"],
        )
        entries_list.append(entry)

    get_session.add_all(entries_list)
    await get_session.commit()

    yield entries_list

    for entry in entries_list:
        query = delete(Entries).where(
            and_(
                Entries.id == entry.id,
                Entries.user_id == entry.user_id,
                Entries.date_start == entry.date_start,
                Entries.date_end == entry.date_end,
                Entries.text == entry.text,
                Entries.status == entry.status,
            )
        )

        await get_session.execute(query)
        await get_session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def authenticated_ac():
    async with AsyncClient(
        base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)
    ) as ac:
        await ac.post(
            "/auth/login",
            json={"email": "user@example.com", "password": "parol"},
        )
        assert ac.cookies["access_token"]
        yield ac


@pytest.fixture(scope="function")
async def authenticated_ac_admin():
    async with AsyncClient(
        base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)
    ) as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "test@test.com",
                "password": "kolobok",
            },
        )
        assert ac.cookies["access_token"]
        yield ac
