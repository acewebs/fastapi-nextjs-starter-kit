import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class RecordCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=5000)
    status: str = Field("pending", max_length=50)


class RecordUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=5000)
    status: str | None = Field(None, max_length=50)


class RecordResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RecordItemResponse(BaseModel):
    item: RecordResponse


class RecordListResponse(BaseModel):
    items: list[RecordResponse]
    total: int


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
