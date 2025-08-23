from dataclasses import dataclass


@dataclass
class CreateTagInputDto:
    name: str


@dataclass
class CreateTagOutputDto:
    id: int
    is_success: bool
    error_message: str
