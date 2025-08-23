from typing import List, Dict, Any
from dataclasses import asdict

from src.domain.dto.notification_dto.get_notifications import GetNotificationsInputDto, GetNotificationsOutputDto
from src.domain.dto.notification_dto.create_notification import CreateNotificationInputDto, CreateNotificationOutputDto


class NotificationAdapter:
    @classmethod
    def request_to_get_notifications_input_dto(cls, user_id: int) -> GetNotificationsInputDto:
        return GetNotificationsInputDto(user_id=user_id)

    @classmethod
    def request_to_create_notification_input_dto(cls, user_id: int, text: str) -> CreateNotificationInputDto:
        return CreateNotificationInputDto(user_id=user_id, text=text)

    @classmethod
    def get_notifications_output_dto_to_response(cls, output_dto: List[GetNotificationsOutputDto]) -> Dict[str, Any]:
        return {"notifications": [asdict(item) for item in output_dto]}

    @classmethod
    def create_notification_output_dto_to_response(cls, output_dto: CreateNotificationOutputDto) -> Dict[str, Any]:
        return asdict(output_dto)
