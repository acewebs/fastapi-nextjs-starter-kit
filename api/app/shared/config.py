from urllib.parse import urlparse

from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    APP_ENV: str = "development"
    LOG_LEVEL: str = "info"
    DATABASE_URL: str = "postgresql+asyncpg://app:app@localhost:5432/app"
    REDIS_URL: str = "redis://localhost:6379"

    @property
    def redis_host(self) -> str:
        return urlparse(self.REDIS_URL).hostname or "localhost"

    @property
    def redis_port(self) -> int:
        return urlparse(self.REDIS_URL).port or 6379

    @property
    def redis_password(self) -> str | None:
        return urlparse(self.REDIS_URL).password

    @property
    def redis_database(self) -> int:
        path = urlparse(self.REDIS_URL).path
        return int(path.lstrip("/") or 0)

    model_config = {"env_file": ".env", "extra": "ignore"}
