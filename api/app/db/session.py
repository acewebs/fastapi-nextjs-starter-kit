from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.shared.db import create_engine, create_session_factory

engine = create_engine(settings.DATABASE_URL, echo=settings.APP_ENV == "development")
async_session = create_session_factory(engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
