import uvicorn
from app.config import settings
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.API_HOST, port=int(settings.PORT), log_level="info")