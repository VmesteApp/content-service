from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class UploadImageInputDto:
    pulse_id: int
    user_id: int
    files: List[bytes]
    filenames: List[str]


@dataclass
class UploadImageOutputDto:
    is_success: bool
    error_message: str
