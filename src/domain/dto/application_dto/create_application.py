from dataclasses import dataclass


@dataclass
class CreateApplicationInputDto:
    pulse_id: int
    candidate_id: int
    message: str


@dataclass
class CreateApplicationOutputDto:
    id: int
    is_success: bool
    error_message: str
