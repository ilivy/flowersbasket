import pytest

from sqlalchemy import create_engine

from app.repository.models import Base
from app.config import settings


engine = create_engine(
    # settings.psycopg2_database_dsn + "_test",
    settings.psycopg2_database_dsn,
    echo=settings.DB_ECHO_LOG,
)


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
