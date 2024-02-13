import uvicorn
from uvicorn.main import logger

from resources.api import app
from config.settings import settings

if __name__ == "__main__":
    logger.info("Starting server ......")
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.log_level
    )