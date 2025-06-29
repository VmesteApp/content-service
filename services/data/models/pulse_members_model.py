from sqlalchemy import Column, Integer, ForeignKey

from services.data.db_session.session import SqlAlchemyBase


class PulseMembersModelORM(SqlAlchemyBase):
    __tablename__ = 'pulse_members'

    id = Column(Integer, primary_key=True)
    pulse_id = Column(Integer, ForeignKey("pulses.id", ondelete="CASCADE"))
    user_id = Column(Integer, nullable=False)

    # def __repr__(self):
    #     return f"<PulseMembers(id={self.id}, name={self.name}, category={self.category})>"
