from typing import List
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from services.data.models.notification_model import NotificationModelORM as notifications_table

from src.domain.entities.notification import Notification
from src.domain.dto.notification_dto.get_notifications import GetNotificationsOutputDto
from src.domain.interfaces.notification_repository import NotificationRepository


class DataBaseNotificationRepository(NotificationRepository):
    def __init__(self, db_session: Session) -> None:
        self.session = db_session

    def get_user_notifications(self, user_id: int) -> List[GetNotificationsOutputDto]:
        try:
            stmt = (
                select(notifications_table)
                .where(notifications_table.user_id == user_id)
                .order_by(notifications_table.created_at.desc())
            )
            
            notifications = self.session.execute(stmt).scalars().all()
            
            return [
                GetNotificationsOutputDto(
                    id=notification.id,
                    user_id=notification.user_id,
                    text=notification.text,
                    created_at=notification.created_at.isoformat()
                )
                for notification in notifications
            ]
        except Exception as error:
            raise Exception(f"Failed to get notifications: {str(error)}")

    def create_notification(self, notification: Notification) -> int:
        try:
            stmt = (
                insert(notifications_table)
                .values({
                    "user_id": notification.user_id,
                    "text": notification.text
                })
                .returning(notifications_table.id)
            )
            
            result = self.session.execute(stmt)
            notification_id = result.scalar_one()
            self.session.commit()
            
            return notification_id
            
        except Exception as error:
            self.session.rollback()
            raise Exception(f"Failed to create notification: {str(error)}")
