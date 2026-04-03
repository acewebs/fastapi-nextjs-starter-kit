import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.record import (
    RecordCreate,
    RecordItemResponse,
    RecordListResponse,
    RecordResponse,
    RecordUpdate,
)
from app.services.record import (
    create_record,
    delete_record,
    get_record,
    list_records,
    update_record,
)

router = APIRouter(prefix="/api/v1/records", tags=["records"])


@router.get("", response_model=RecordListResponse)
async def list_records_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    items, total = await list_records(db, skip=skip, limit=limit)
    return RecordListResponse(items=[RecordResponse.model_validate(i) for i in items], total=total)


@router.post("", response_model=RecordItemResponse, status_code=201)
async def create_record_route(data: RecordCreate, db: AsyncSession = Depends(get_db)):
    record = await create_record(db, data)
    return RecordItemResponse(item=RecordResponse.model_validate(record))


@router.get("/{record_id}", response_model=RecordItemResponse)
async def get_record_route(record_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    record = await get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return RecordItemResponse(item=RecordResponse.model_validate(record))


@router.patch("/{record_id}", response_model=RecordItemResponse)
async def update_record_route(record_id: uuid.UUID, data: RecordUpdate, db: AsyncSession = Depends(get_db)):
    record = await get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    updated = await update_record(db, record, data)
    return RecordItemResponse(item=RecordResponse.model_validate(updated))


@router.delete("/{record_id}", status_code=204)
async def delete_record_route(record_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    record = await get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    await delete_record(db, record)
