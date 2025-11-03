from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetImageInputDto:
    image_uuid: UUID


@dataclass
class GetImageOutputDto:
    file_path: str
    is_success: bool
    error_message: str
