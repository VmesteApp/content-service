from dataclasses import dataclass

from src.domain.entities.pulse import Pulse


@dataclass
class GetUserApplicationInputDto:
    user_id: int


@dataclass
class GetUserApplicationOutputDto:
    id: int
    pulse: Pulse
    message: str
    status: str
