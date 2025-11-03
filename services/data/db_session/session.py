import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
import sqlalchemy.ext.declarative as dec

from services.data.config import DB_URL


SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    engine = sa.create_engine(DB_URL, echo=False)

    __factory = sessionmaker(bind=engine)

    from services.data.db_session import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    return __factory()
