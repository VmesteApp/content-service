from dataclasses import dataclass


@dataclass
class UpdateApplicationInputDto:
    id: int
    status: str


@dataclass
class UpdateApplicationOutputDto:
    is_success: bool
    error_message: str
