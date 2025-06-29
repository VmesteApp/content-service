from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from services.data.db_session.session import SqlAlchemyBase


class PulseORM(SqlAlchemyBase):
    __tablename__ = 'pulses'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    founder_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    short_description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    blocked = Column(Boolean, default=False)

    # def __repr__(self):
    #     return (
    #         f"<PulseORM(id={self.id}, category='{self.category}', name='{self.name}', "
    #         f"founder_id={self.founder_id}, created_at='{self.created_at}', "
    #         f"updated_at='{self.updated_at}', blocked={self.blocked})>"
    #     )

