from typing import List
from src.domain.dto.notification_dto.get_notifications import GetNotificationsInputDto, GetNotificationsOutputDto
from src.domain.interfaces.notification_repository import NotificationRepository


class GetNotifications:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: GetNotificationsInputDto) -> List[GetNotificationsOutputDto]:
        try:
            return self.repository.get_user_notifications(dto.user_id)
        except Exception as error:
            raise Exception(f"Failed to get notifications: {str(error)}")
