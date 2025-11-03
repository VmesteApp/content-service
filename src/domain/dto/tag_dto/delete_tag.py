from dataclasses import dataclass


@dataclass
class DeleteTagInputDto:
    id: int


@dataclass
class DeleteTagOutputDto:
    is_success: bool
    error_message: str
