from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "mail_manager"
    APP_VERSION: str = "0.01"
    LOG_LEVEL: str = "INFO"
    UVICORN_DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DB_URL: str = "sqlite:///./test.db"
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_DATABASE_TYPE: str = "sqlite"

    # set settings via env vars using env_prefix, e.g. to set LOG_LEVEL use env var "MAIL_MANAGER_"LOG_LEVEL
    model_config = SettingsConfigDict(env_prefix="MAIL_MANAGER_")


# singleton
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
