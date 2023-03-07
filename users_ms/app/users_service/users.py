"""
Business logic layers.
Models.
"""
import uuid
from typing import Optional

from app.repository.models import UserModel


class User:
    def __init__(
        self,
        id: uuid,
        username: str,
        email: str,
        user_: Optional[UserModel] = None,
    ):
        self._id = id
        self.username = username
        self.email = email
        self._user = user_  # in case of a new Instance will be used to fetch ID

    @property
    def id(self):
        return self._id or self._user.id

    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
