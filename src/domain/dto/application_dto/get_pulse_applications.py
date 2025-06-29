from dataclasses import dataclass

from src.domain.entities.pulse import Pulse


@dataclass
class GetPulseApplicationInputDto:
    pulse_id: int


@dataclass
class GetPulseApplicationOutputDto:
    id: int
    pulse: Pulse
    message: str
    status: str
