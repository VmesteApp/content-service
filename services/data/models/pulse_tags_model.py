from sqlalchemy import Column, Integer, ForeignKey

from services.data.db_session.session import SqlAlchemyBase


class PulseTagsModelORM(SqlAlchemyBase):
    __tablename__ = 'pulse_tags'

    id = Column(Integer, primary_key=True)
    pulse_id = Column(Integer, ForeignKey("pulses.id", ondelete="CASCADE"))
    tag_id = Column(Integer)

    # def __repr__(self):
    #     return f"<PulseTags(id={self.id}, pulse_id={self.pulse_id}, tag_id={self.tag_id})>"
