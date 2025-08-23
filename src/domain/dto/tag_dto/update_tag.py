from dataclasses import dataclass


@dataclass
class UpdateTagInputDto:
    id: int
    name: str


@dataclass
class UpdateTagOutputDto:
    is_success: bool
    error_message: str
