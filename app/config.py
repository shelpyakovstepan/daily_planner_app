# STDLIB
import os
from typing import Literal

# THIRDPARTY
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "PROD", "TEST"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DB_HOST: str = "${DB_HOST}"
    DB_PORT: int = "${DB_PORT}"
    DB_USER: str = "${DB_USER}"
    DB_PASS: str = "${DB_PASS}"
    DB_NAME: str = "${DB_NAME}"

    TEST_DB_HOST: str = "${TEST_DB_HOST}"
    TEST_DB_PORT: int = "${TEST_DB_PORT}"
    TEST_DB_USER: str = "${TEST_DB_USER}"
    TEST_DB_PASS: str = "${TEST_DB_PASS}"
    TEST_DB_NAME: str = "${TEST_DB_NAME}"

    RABBIT_USER: str = "${RABBIT_USER}"
    RABBIT_PASS: str = "${RABBIT_PASS}"
    RABBIT_HOST: str = "${RABBIT_HOST}"
    RABBIT_PORT: int = "${RABBIT_PORT}"

    SMTP_HOST: str = "${SMTP_HOST}"
    SMTP_PORT: int = "${SMTP_PORT}"
    SMTP_USER: str = "${SMTP_USER}"
    SMTP_PASS: str = "${SMTP_PASS}"

    SECRET_KEY: str = "${SECRET_KEY}"
    ALGORITHM: str = "${ALGORITHM}"

   #model_config = SettingsConfigDict(
   #     env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
   # )


settings = Settings()  # pyright: ignore [reportCallIssue]
