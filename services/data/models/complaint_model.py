from sqlalchemy import Column, Integer, String, ForeignKey

from services.data.db_session.session import SqlAlchemyBase


class ComplaintModelORM(SqlAlchemyBase):
    __tablename__ = 'complaints'

    id = Column(Integer, primary_key=True)
    pulse_id = Column(Integer, ForeignKey("pulses.id", ondelete="CASCADE"))
    message = Column(String, nullable=True)
    status = Column(String, default="PENDING")

    # def __repr__(self):
    #     return f"<Complaint(id={self.id}, name={self.name}, category={self.category})>"
