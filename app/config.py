from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str = Field(default='itech_fastapi_db', env='POSTGRES_DB')
    POSTGRES_USER: str = Field(default='postgres', env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(default='12345', env='POSTGRES_PASSWORD')
    POSTGRES_HOST: str = Field(default='127.0.0.1', env='POSTGRES_HOST')
    POSTGRES_PORT: int = Field(default=5432, env='POSTGRES_PORT')

    REDIS_HOST: str = Field(default='redis', env='REDIS_HOST')
    REDIS_PORT: int = Field(default=6379, env='REDIS_PORT')

    REPOSITORY_TYPE: str = Field(default='orm', env='REPOSITORY_TYPE')



settings = Settings()
