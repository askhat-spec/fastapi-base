from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from .services import access_security, refresh_security, AuthService, UserService
from .schemas import UserCreate, User, Tokens, UserLogin


auth_router = APIRouter()

users_router = APIRouter()


@auth_router.post('/register', response_model=Tokens)
async def register(user_data: UserCreate, service: AuthService = Depends()):
    return await service.create_user(user_data)


@auth_router.post('/login', response_model=Tokens)
async def login(user_data: UserLogin, service: AuthService = Depends()):
    return await service.authenticate(user_data)


@auth_router.post("/refresh", response_model=Tokens)
def refresh(
    credentials: HTTPAuthorizationCredentials = Security(refresh_security),
    service: AuthService = Depends()
):
    return service.create_tokens(User.model_validate(credentials.subject))


@users_router.get('/', response_model=list[User])
async def get_users(
    credentials: HTTPAuthorizationCredentials = Security(access_security),
    service: UserService = Depends()
):
    return await service.get_users(User.model_validate(credentials.subject))


@users_router.get('/me', response_model=User)
async def get_me(
    credentials: HTTPAuthorizationCredentials = Security(access_security),
    service: UserService = Depends()
):
    return await service.get_one(User.model_validate(credentials.subject))
