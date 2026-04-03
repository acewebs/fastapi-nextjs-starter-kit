from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

from app.core.config import settings

_arq_pool: ArqRedis | None = None


def _redis_settings() -> RedisSettings:
    return RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        database=settings.redis_database,
    )


async def init_redis() -> None:
    global _arq_pool
    _arq_pool = await create_pool(_redis_settings())


async def close_redis() -> None:
    global _arq_pool
    if _arq_pool:
        await _arq_pool.aclose()
        _arq_pool = None


def get_arq_pool() -> ArqRedis:
    if _arq_pool is None:
        raise RuntimeError("ARQ Redis pool not initialized")
    return _arq_pool
