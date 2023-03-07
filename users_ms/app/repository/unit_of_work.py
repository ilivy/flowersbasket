from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


class UnitOfWork:
    def __init__(self):
        engine = create_engine(
            settings.psycopg2_database_dsn,
            echo=settings.DB_ECHO_LOG,
        )
        """
        a pointer to the sessionmaker factory function of SQLAlchemy
        """
        self.session_maker = sessionmaker(engine, expire_on_commit=False)

    def __enter__(self):
        """
        On entering the Unit of Work context,
        we get an instance of SQLAlchemy’s session object
        """
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        If an exception took place, we must roll back all the transactions
        accumulated in the session object to avoid leaving
        the database in an inconsistent state
        """
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self):
        """
        Wrapper around the commit() method from SQLAlchemy’s session object.
        If we were working with more than one database,
        we could handle all commits within this method.
        """
        self.session.commit()

    def rollback(self):
        """
        Wrapper around the rollback() method from SQLAlchemy’s session object.
        If we were working with more than one database,
        we could handle all rollbacks within this method
        """
        self.session.rollback()
