from uuid import UUID

from email_validator import validate_email as validate_eml, EmailNotValidError
from pydantic import BaseModel, Extra, validator, root_validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class EmailField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        try:
            validate_eml(v)
            return v
        except EmailNotValidError:
            raise ValueError("Email is not valid.")


class BaseUserSchema(BaseModel):
    username: str
    email: EmailField

    # class Config:
    #     extra = Extra.forbid


class UserRegisterInSchema(BaseUserSchema):
    password: str
    password_confirm: str

    @validator("username")
    def username_alphanumeric(cls, value):
        assert len(value) > 0, "Username cannot be empty."
        assert len(value) < 120, "Username cannot be longer than 120 characters."
        assert value.isalnum(), "Username must be alphanumeric."
        return value

    @validator("password")
    def password_not_empty(cls, value):
        assert len(value) > 0, "Password cannot be empty."
        return value

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("password_confirm")

        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        return values


class UserLoginInSchema(BaseUserSchema):
    password: str


class UserSchema(BaseUserSchema):
    id: UUID


class UserOutSchema(UserSchema):
    pass
