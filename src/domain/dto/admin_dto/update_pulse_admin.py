from dataclasses import dataclass


@dataclass
class UpdatePulseAdminInputDto:
    id: int
    category: str
    name: str
    description: str
    short_description: str
    tags: str


@dataclass
class UpdatePulseAdminOutputDto:
    is_success: bool
    error_message: str
