from dataclasses import dataclass

from src.domain.entities.pulse import Pulse


@dataclass
class GetPulseApplicationsInputDto:
    pulse_id: int


@dataclass
class GetPulseApplicationsOutputDto:
    pulse_id: int
    candidate_id: int
    application_id: int
    message: str
    status: str
