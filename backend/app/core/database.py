from typing import Generator

from sqlalchemy import create_engine, event, URL
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

SQLALCHEMY_DATABASE_URL=URL.create(
    drivername="sqlite",
    database="./task_manager.db",
)

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
)

@event.listens_for(Engine,"connect")
def set_sqlite_pragma(dbapi_connection,connection_record) -> None:
    cursor=dbapi_connection.cursos()
    cursor.execute("PRAGMA foreign_keys=ON")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session,None,None]:
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()