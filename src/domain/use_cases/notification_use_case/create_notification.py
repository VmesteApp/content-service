from src.domain.dto.notification_dto.create_notification import CreateNotificationInputDto, CreateNotificationOutputDto
from src.domain.entities.notification import Notification
from src.domain.interfaces.notification_repository import NotificationRepository


class CreateNotification:
    def __init__(self, repository: NotificationRepository) -> None:
        self.repository = repository
    
    def execute(self, dto: CreateNotificationInputDto) -> CreateNotificationOutputDto:
        try:
            notification = Notification(
                id=None,
                user_id=dto.user_id,
                text=dto.text,
                created_at=None
            )
            
            notification_id = self.repository.create_notification(notification)
            
            return CreateNotificationOutputDto(
                id=notification_id,
                is_success=True,
                error_message=""
            )
            
        except Exception as error:
            return CreateNotificationOutputDto(
                id=None,
                is_success=False,
                error_message=str(error)
            )
