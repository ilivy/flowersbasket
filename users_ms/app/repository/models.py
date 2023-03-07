"""
Data layer.
Models.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column


def generate_uuid():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    username: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
