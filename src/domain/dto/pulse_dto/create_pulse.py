from dataclasses import dataclass


@dataclass
class CreatePulseInputDto:
    category: str
    name: str
    founder_id: int
    description: str
    short_description: str
    tags: str

@dataclass
class CreatePulseOutputDto:
    id: int
    is_success: bool
    error_message: str
