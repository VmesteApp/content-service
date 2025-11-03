from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Image:
    image_id: Optional[UUID]
    pulse_id: int
    full_name: str
    image_path: str
