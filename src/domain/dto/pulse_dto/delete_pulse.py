from dataclasses import dataclass


@dataclass
class DeletePulseInputDto:
    pulse_id: int


@dataclass
class DeletePulseOutputDto:
    is_success: bool
    error_message: str
