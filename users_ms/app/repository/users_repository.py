"""
Data layer.
Repository.
"""
from sqlalchemy.sql.expression import select

from app.users_service.users import User
from app.repository.models import UserModel


class UsersRepository:
    def __init__(self, session):
        self.session = session

    def add(self, username, email, password) -> User:
        record = UserModel(username=username, email=email, password=password)
        self.session.add(record)
        return User(**record.dict(), user_=record)

    def find_by_username(self, username) -> UserModel:
        return self.session.scalar(
            select(UserModel).where(UserModel.username == username)
        )

    def find_by_email(self, email) -> UserModel:
        return self.session.scalar(select(UserModel).where(UserModel.email == email))
