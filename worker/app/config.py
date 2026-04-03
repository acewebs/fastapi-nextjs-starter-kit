from arq.connections import RedisSettings

from app.shared.config import BaseAppSettings


class Settings(BaseAppSettings):
    @property
    def redis_settings(self) -> RedisSettings:
        return RedisSettings(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password,
            database=self.redis_database,
        )


settings = Settings()
