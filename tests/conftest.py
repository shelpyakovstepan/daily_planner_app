# STDLIB
from datetime import datetime
import json

# THIRDPARTY
import httpx
from celery import Celery
from httpx import AsyncClient
from kombu import Connection
import pytest
from sqlalchemy import insert

# FIRSTPARTY
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.entries.models import Entries
from app.logger import logger
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    entries = open_mock_json("entries")

    for entry in entries:
        entry["date_start"] = datetime.strptime(entry["date_start"], "%Y-%m-%d")
        entry["date_end"] = datetime.strptime(entry["date_end"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_entries = insert(Entries).values(entries)

        await session.execute(add_users)
        await session.execute(add_entries)

        await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def prepare_rabbitmq_and_celery():
    assert settings.MODE == "TEST"

    conn_url = (
        f"amqp://{settings.TEST_RABBIT_USER}:{settings.TEST_RABBIT_PASS}@"
        f"{settings.TEST_RABBIT_HOST}:{settings.TEST_RABBIT_PORT}/"
    )
    try:
        with Connection(conn_url) as conn:
            conn.connect()
            logger.info("Successfully connected to RabbitMQ")
            celery = Celery(
                "tasks",
                broker=f"amqp://{settings.TEST_RABBIT_USER}:{settings.TEST_RABBIT_PASS}@"
                       f"{settings.TEST_RABBIT_HOST}:{settings.TEST_RABBIT_PORT}/",
                include=["app.tasks.tasks"],
            )
    except Exception as e:
        logger.error(f"RabbitMQ and Celery connection failed: {str(e)}", exc_info=True)


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
async def authenticated_ac_admin():
    async with AsyncClient(
        base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)
    ) as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "step3210shelpyakov@gmail.com",
                "password": "kolobok",
            },
        )
        assert ac.cookies["access_token"]
        yield ac
