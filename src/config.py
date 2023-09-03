from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    SERVER_HOST: str = 'localhost'
    SERVER_PORT: int = 8000
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    JWT_SECRET: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_TIME: int = 60 * 5
    JWT_REFRESH_TOKEN_TIME: int = 60 * 60 * 24 * 7

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
