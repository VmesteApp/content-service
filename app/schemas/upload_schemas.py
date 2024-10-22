from uuid import UUID
from pydantic import BaseModel


class DeleteImage(BaseModel):
    image_id: UUID

class UploadNewFile(BaseModel):
    id: int
    file_id: UUID
    file_path: str
