import uvicorn
from mail_manager.settings import settings

uvicorn.run(
    "mail_manager.main:app",
    host=settings.HOST,
    port=settings.PORT,
    reload=False,
)
