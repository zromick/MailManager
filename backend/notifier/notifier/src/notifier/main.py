import asyncio
from contextlib import asynccontextmanager

from app_common.logger import logger
from fastapi import FastAPI
from notifier.core.v1.notifier import get_notification_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    notifier_instance = get_notification_manager()
    polling_task = asyncio.create_task(notifier_instance.start_polling())
    logger.info("Notifier polling task started.")
    yield
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        logger.info("Notifier polling task cancelled during shutdown.")
    logger.info("Notifier polling task stopped.")


def get_application():
    application = FastAPI(lifespan=lifespan)
    return application


app = get_application()
