from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Notification:
    id: Optional[int]
    user_id: int
    text: str
    created_at: Optional[datetime]
