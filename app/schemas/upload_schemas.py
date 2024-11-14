from typing import List, Union
from uuid import UUID
from pydantic import BaseModel


class DeleteImage(BaseModel):
    image_id: UUID

class UploadNewFile(BaseModel):
    images: List[str]
