from datetime import timedelta
from typing import Any, Dict
from fastapi import HTTPException, status
from fastapi_jwt import (
    JwtAccessBearerCookie,
    JwtRefreshBearerCookie,
)
from tortoise.exceptions import IntegrityError
from passlib.context import CryptContext

from .schemas import UserCreate, User, Tokens, UserLogin
from .models import UserModel
from src.config import settings


access_security = JwtAccessBearerCookie(
    secret_key=settings.JWT_SECRET,
    access_expires_delta=timedelta(seconds=settings.JWT_ACCESS_TOKEN_TIME)
)

refresh_security = JwtRefreshBearerCookie(
    secret_key=settings.JWT_SECRET,
    refresh_expires_delta=timedelta(seconds=settings.JWT_REFRESH_TOKEN_TIME)
)


class AuthService:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_user(self, user_data: UserCreate) -> Tokens:
        try:
            user = await UserModel.create(
                **user_data.model_dump(exclude_unset=True, exclude=['password']),
                password=self.hash_password(user_data.password.get_secret_value())
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        payload = User.model_validate(user).model_dump(mode='json')
        return self.create_tokens(payload)

    async def authenticate(self, user_data: UserLogin):
        user = await UserModel.filter(email=user_data.email, is_active=True).first()
        if user is None or not self.verify_password(user_data.password.get_secret_value(), user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password',
            )
        payload = User.model_validate(user).model_dump(mode='json')
        return self.create_tokens(payload)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.password_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.password_context.verify(plain_password, hashed_password)

    @classmethod
    def create_tokens(cls, payload: Dict[str, Any]) -> Tokens:
        return Tokens(
            access_token=access_security.create_access_token(payload),
            refresh_token=refresh_security.create_refresh_token(payload)
        )


class UserService:
    async def get_users(self, user: User) -> list[User]:
        user = await UserModel.get(id=user.id)
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Permission denied'
            )
        return await UserModel.all()

    async def get_one(self, user: User) -> User:
        return await UserModel.get(id=user.id)
