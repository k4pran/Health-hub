from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import database

engine = create_engine(
    "sqlite:///devdata.db",
    echo=True
)

database.Base.metadata.create_all(engine)

SessionMaker = sessionmaker(bind=engine)


def get_session() -> Session:
    return SessionMaker()
