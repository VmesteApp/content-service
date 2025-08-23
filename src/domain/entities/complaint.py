from dataclasses import dataclass
from typing import Optional


@dataclass
class Complaint:
    id: Optional[int]
    pulse_id: int
    message: str
    status: Optional[str] = "PENDING"
