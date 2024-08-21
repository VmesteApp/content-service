import os
from app.config import DATABASE_URL

from sqlmodel import create_engine, SQLModel, Session

engine = create_engine(DATABASE_URL, echo=True, future=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session