import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker

from mail_manager.settings import settings

metadata = sqlalchemy.MetaData()

if settings.DB_DATABASE_TYPE == "sqlite":
    engine = sqlalchemy.create_engine(
        settings.DB_URL, connect_args={"check_same_thread": False}, echo=True
    )
else:
    engine = sqlalchemy.create_engine(
        settings.DB_URL,
    )

# Create a session class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
