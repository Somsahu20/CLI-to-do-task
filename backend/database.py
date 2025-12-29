from .config import settings
SQL_STRING = f"postgresql://{settings.db_user}:{settings.password}@{settings.db_host}/{settings.db_name}"

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(SQL_STRING, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()