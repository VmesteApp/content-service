from dataclasses import dataclass


@dataclass
class CreateComplaintInputDto:
    pulse_id: int
    message: str


@dataclass
class CreateComplaintOutputDto:
    is_success: bool
    error_message: str
