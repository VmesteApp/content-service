from dataclasses import dataclass


@dataclass
class CreatePulseAdminInputDto:
    category: str
    name: str
    description: str
    short_description: str
    user_id: int
    tags: str


@dataclass
class CreatePulseAdminOutputDto:
    pulse_id: int
    is_success: bool
    error_message: str
