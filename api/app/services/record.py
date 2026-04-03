import logging
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import get_arq_pool
from app.models import Record
from app.schemas.record import RecordCreate, RecordUpdate

logger = logging.getLogger(__name__)


async def create_record(db: AsyncSession, data: RecordCreate) -> Record:
    record = Record(**data.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    await _enqueue_job("process_record", str(record.id))
    return record


async def get_record(db: AsyncSession, record_id: uuid.UUID) -> Record | None:
    return await db.get(Record, record_id)


async def list_records(db: AsyncSession, skip: int = 0, limit: int = 50) -> tuple[list[Record], int]:
    total_result = await db.execute(select(func.count(Record.id)))
    total = total_result.scalar_one()

    result = await db.execute(select(Record).order_by(Record.created_at.desc()).offset(skip).limit(limit))
    items = list(result.scalars().all())
    return items, total


async def update_record(db: AsyncSession, record: Record, data: RecordUpdate) -> Record:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    await db.commit()
    await db.refresh(record)
    return record


async def delete_record(db: AsyncSession, record: Record) -> None:
    await db.delete(record)
    await db.commit()


async def _enqueue_job(job_name: str, record_id: str) -> None:
    try:
        pool = get_arq_pool()
        await pool.enqueue_job(job_name, record_id)
        logger.info("Enqueued job %s for record %s", job_name, record_id)
    except Exception:
        logger.warning("Failed to enqueue job %s for record %s — Redis may be unavailable", job_name, record_id)
