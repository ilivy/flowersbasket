from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(
    settings.psycopg2_database_dsn,
    echo=settings.DB_ECHO_LOG,
)

session = sessionmaker(
    bind=engine, expire_on_commit=False, autocommit=False, autoflush=False
)
