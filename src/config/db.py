from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings
USER_DB = settings.POSTGRES_USER
PASSWORD_DB = settings.POSTGRES_PASSWORD
HOST_DB = settings.HOST_DB
NAME_DB = settings.POSTGRES_DB

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:5432/{NAME_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
