from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"

    # set settings via env vars using env_prefix, e.g. to set LOG_LEVEL use env var "MAIL_MANAGER_SDK_"LOG_LEVEL
    model_config = SettingsConfigDict(env_prefix="MAIL_MANAGER_SDK_")


# singleton
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
