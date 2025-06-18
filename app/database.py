# THIRDPARTY
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# FIRSTPARTY
from app.config import settings
from app.logger import logger

if settings.MODE == "TEST":
    DATABASE_URL = (f"postgresql+asyncpg://{settings.TEST_DB_USER}:"
                    f"{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:"
                    f"{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}")
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = (f"postgresql+asyncpg://{settings.DB_USER}:"
                    f"{settings.DB_PASS}@{settings.DB_HOST}:"
                    f"{settings.DB_PORT}/{settings.DB_NAME}")
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def check_db_connection():
    try:
        async with AsyncSession(engine) as session:
            await session.execute(text("SELECT 1"))
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Unsuccessful connection to database: {e}", exc_info=True)
        raise e


class Base(DeclarativeBase):
    pass
