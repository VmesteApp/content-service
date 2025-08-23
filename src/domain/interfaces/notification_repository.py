from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.notification import Notification
from src.domain.dto.notification_dto.get_notifications import GetNotificationsOutputDto


class NotificationRepository(ABC):
    @abstractmethod
    def get_user_notifications(self, user_id: int) -> List[GetNotificationsOutputDto]:
        pass
    
    @abstractmethod
    def create_notification(self, notification: Notification) -> int:
        pass
