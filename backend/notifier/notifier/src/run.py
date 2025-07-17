import uvicorn
from notifier.settings import settings

uvicorn.run(
    "notifier.main:app",
    host=settings.HOST,
    port=settings.PORT,
    reload=False,
)
