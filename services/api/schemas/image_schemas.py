from pydantic import BaseModel
from uuid import UUID


class ImageResponseSchema(BaseModel):
    image_id: UUID
    pulse_id: int
    image_path: str

    class Config:
        from_attributes = True
