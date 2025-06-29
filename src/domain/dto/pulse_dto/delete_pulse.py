from dataclasses import dataclass


@dataclass
class DeletePulseInputDto:
    id: int


@dataclass
class DeletePulseOutputDto:
    is_success: bool
    error_message: str
