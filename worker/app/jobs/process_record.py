import asyncio
import logging

from app.config import settings
from app.shared.db import create_engine, create_session_factory
from app.shared.models.record import Record

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)
async_session = create_session_factory(engine)


async def process_record(ctx: dict, record_id: str) -> str:
    logger.info("Processing record %s", record_id)

    # Update status to processing
    async with async_session() as session:
        record = await session.get(Record, record_id)
        if not record:
            logger.warning("Record %s not found, skipping", record_id)
            return f"Record {record_id} not found"
        record.status = "processing"
        await session.commit()

    # Simulate async work (e.g., external API call, heavy computation)
    await asyncio.sleep(2)

    # Mark as completed
    async with async_session() as session:
        record = await session.get(Record, record_id)
        if record:
            record.status = "completed"
            await session.commit()

    logger.info("Completed processing record %s", record_id)
    return f"Processed {record_id}"
