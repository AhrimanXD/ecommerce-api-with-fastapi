from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY = "834c870359268867c4dd14c973a14d637d453df1941f73788d6a69a1bb0c8614"
    ALGORITHM = "HS256"
    PROJECT_TITLE = ""
    DATABASE_URL = "postgresql://postgres:changethis@db/app"
    DEV = False
    TOKEN_LIFESPAN = 30

    model_config = SettingsConfigDict(env_file='', env_file_encoding='utf-8')

@lru_cache()
def get_settings():
    return Settings()

settings = Settings()

