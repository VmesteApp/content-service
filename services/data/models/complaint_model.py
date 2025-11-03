from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from services.data.db_session.session import SqlAlchemyBase


class ComplaintModelORM(SqlAlchemyBase):
    __tablename__ = 'complaints'

    id = Column(Integer, primary_key=True)
    pulse_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Complaint(id={self.id}, pulse_id={self.pulse_id}, status={self.status})>"
