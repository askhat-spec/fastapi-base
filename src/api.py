from fastapi import APIRouter

from src.auth.controllers import auth_router, users_router


main_router = APIRouter(prefix='/api')

main_router.include_router(auth_router, prefix='/auth', tags=['Auth'])
main_router.include_router(users_router, prefix='/users', tags=['Users'])
