from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from datetime import datetime


class UUIDModel(SQLModel):
    uu_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        unique_items=True
    )
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        default_factory=datetime.now)
