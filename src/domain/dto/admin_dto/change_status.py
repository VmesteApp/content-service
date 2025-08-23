from dataclasses import dataclass


@dataclass
class ChangeStatusInputDto:
    pulse_id: int
    blocked: bool


@dataclass
class ChangeStatusOutputDto:
    is_success: bool
    error_message: str
