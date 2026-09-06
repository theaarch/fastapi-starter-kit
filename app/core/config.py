import logging
import secrets
from pathlib import Path
from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_PREFIX: str = "/api"
    APP_NAME: str = "FastAPI Starter Kit"
    APP_URL: str = "http://localhost:8000"
    CORS_ORIGINS: list[str] = ["*"]

    # JWT Settings
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRATION: int = 60 * 24  # in minutes

    # Database Settings (PostgreSQL asyncpg default)
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db"

    @model_validator(mode="after")
    def validate_secret_key(self) -> Self:
        if not self.SECRET_KEY:
            logger.warning(
                "SECRET_KEY is not set in environment or .env! Generating an ephemeral random secret. "
                "Sessions will be invalidated on server restart. DO NOT use in production!"
            )
            self.SECRET_KEY = secrets.token_urlsafe(32)
        return self


settings = Settings()
