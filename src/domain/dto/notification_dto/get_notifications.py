from dataclasses import dataclass


@dataclass
class GetNotificationsInputDto:
    user_id: int


@dataclass
class GetNotificationsOutputDto:
    id: int
    user_id: int
    text: str
    created_at: str
