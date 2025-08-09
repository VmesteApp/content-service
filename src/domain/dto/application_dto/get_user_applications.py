from typing import List
from dataclasses import dataclass

from src.domain.entities.pulse import Pulse


@dataclass
class GetUserApplicationsInputDto:
    user_id: int


@dataclass
class GetUserApplicationsOutputDto:
    application_id: int
    pulse: List[Pulse]
    message: str
    status: str
    error_message: str
