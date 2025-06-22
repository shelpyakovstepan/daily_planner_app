# STDLIB
import os
from typing import Literal

# THIRDPARTY
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "PROD", "TEST"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    RABBIT_USER: str
    RABBIT_PASS: str
    RABBIT_HOST: str
    RABBIT_PORT: int

    TEST_RABBIT_USER: str
    TEST_RABBIT_PASS: str
    TEST_RABBIT_HOST: str
    TEST_RABBIT_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()  # pyright: ignore [reportCallIssue]
