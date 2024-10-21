from uuid import UUID
from pydantic import BaseModel


class UploadImage(BaseModel):
    image_id: UUID
    pulse_id: int
