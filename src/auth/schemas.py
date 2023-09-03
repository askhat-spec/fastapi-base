from pydantic import BaseModel, SecretStr, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator
from uuid import UUID

from .models import UserModel


class UserBaseSchema(BaseModel):
    email: EmailStr
    name: str | None = None
    last_name: str | None = None

    class Config:
        from_attributes = True


class UserCreate(UserBaseSchema):
    password: SecretStr


class User(UserBaseSchema):
    id: UUID


UserDBSchema = pydantic_model_creator(UserModel, name="User", exclude=['password'])


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
