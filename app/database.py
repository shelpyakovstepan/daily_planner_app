# THIRDPARTY
from sqlalchemy import text, NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# FIRSTPARTY
from app.config import settings
from app.logger import logger

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASS}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def check_db_connection():
    try:
        async with AsyncSession(engine) as session:
            await session.execute(text("SELECT 1"))
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Unsuccessful connection to database: {e}", exc_info=True)
        raise e


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
