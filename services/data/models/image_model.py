from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey
from sqlalchemy.sql import func

from services.data.db_session.session import SqlAlchemyBase


class ImageModelORM(SqlAlchemyBase):
    __tablename__ = 'images'

    image_id = Column(UUID, primary_key=True)
    pulse_id = Column(Integer, ForeignKey("pulses.id", ondelete="CASCADE"))
    full_name = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Image(id={self.id}, pulse_id={self.pulse_id}>"
