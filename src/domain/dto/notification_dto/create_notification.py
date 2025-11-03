from dataclasses import dataclass


@dataclass
class CreateNotificationInputDto:
    user_id: int
    text: str


@dataclass
class CreateNotificationOutputDto:
    id: int
    is_success: bool
    error_message: str
