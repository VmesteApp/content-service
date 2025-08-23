from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeleteImageInputDto:
    image_uuid: UUID
    user_id: int


@dataclass
class DeleteImageOutputDto:
    is_success: bool
    error_message: str
