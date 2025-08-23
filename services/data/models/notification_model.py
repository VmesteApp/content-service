from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from services.data.db_session.session import SqlAlchemyBase


class NotificationModelORM(SqlAlchemyBase):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, text={self.text[:50]}...)>"
