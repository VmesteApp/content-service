from sqlalchemy import Column, Integer, String

from services.data.db_session.session import SqlAlchemyBase


class TagModelORM(SqlAlchemyBase):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # def __repr__(self):
    #     return f"<Tag(id={self.id}, name={self.name}>"
