from app_common.logger import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from mail_manager.api.v1 import mail_manager_api
from mail_manager.api.v1.exceptions import setup_exception_handlers
from mail_manager.core.v1 import database
from mail_manager.settings import Settings, settings

database.Base.metadata.create_all(bind=database.engine)


def get_application(settings: Settings) -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        debug=settings.UVICORN_DEBUG,
        version=settings.APP_VERSION,
    )

    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(mail_manager_api.router)
    add_pagination(application)

    setup_exception_handlers(application)

    logger.info(settings.model_dump())

    return application


app = get_application(settings)
