"""
Encapsulates the capabilities of the 'users domain'.

API module won’t be using the User class directly.
Instead, we’ll use a unified interface to all
our adapters through the UsersService class
"""
from fastapi import HTTPException
from starlette import status

from app.repository.users_repository import UsersRepository
from app.users_service.users import User
from app.web.api.auth import get_password_hash


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    def add_user(self, username, email, password) -> User:
        # Check if username is not unique
        user_exist = self.users_repo.find_by_username(username)
        if user_exist:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "User with this username already exists"
            )
        # Check if email is not unique
        user_exist = self.users_repo.find_by_email(email)
        if user_exist:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "User with this email already exists"
            )

        password = get_password_hash(password)
        user = self.users_repo.add(username, email, password)

        return user
