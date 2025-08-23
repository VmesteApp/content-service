from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationResponseSchema(BaseModel):
    id: int
    user_id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class CreateNotificationSchema(BaseModel):
    user_id: int
    text: str


class NotificationListResponseSchema(BaseModel):
    notifications: list[NotificationResponseSchema]
