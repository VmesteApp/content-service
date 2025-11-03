from dataclasses import dataclass


@dataclass
class UpdatePulseInputDto:
    id: int
    category: str
    name: str
    description: str
    short_description: str
    tags: str


@dataclass
class UpdatePulseOutputDto:
    is_success: bool
    error_message: str
