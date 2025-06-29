from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from services.data.db_session.session import SqlAlchemyBase


class ApplicationModelORM(SqlAlchemyBase):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    pulse_id = Column(Integer, nullable=False)
    candidate_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # def __repr__(self):
    #     return f"<Application(id={self.id}, candidate_id={self.candidate_id}, status={self.status})>"
