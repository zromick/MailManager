from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "notifier"
    APP_VERSION: str = "0.01"
    LOG_LEVEL: str = "INFO"
    UVICORN_DEBUG: bool = False
    MAIL_MANAGER_BASE_URL: str = "http://localhost:8000"
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    MAIL_ITEM_REVIEW_POLL_INTERVAL_SECONDS: int = 1  # Poll every second
    MAIL_ITEM_REVIEW_NOTIFICATION_INTERVAL_SECONDS: int = (
        # 21600  # Notify every 6 hours (6 * 3600 seconds)
        30  # Notify every half-minute for testing purposes
    )

    # SendGrid Env Variables
    SENDGRID_API_KEY: str = ""
    SENDER_EMAIL: str = "zac.romick@gmail.com"

    # set settings via env vars using env_prefix, e.g. to set LOG_LEVEL use env var "NOTIFIER_"LOG_LEVEL
    model_config = SettingsConfigDict(
        env_prefix="NOTIFIER_",
        env_file=Path(__file__).parent.parent.parent / ".env",
    )


# singleton
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
