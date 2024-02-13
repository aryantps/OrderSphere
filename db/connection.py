from uvicorn.main import logger
from config.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class DbConnectionManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self):

        if not self.client:
            logger.info("Connecting to MongoDB.")
            self.client = AsyncIOMotorClient(
                settings.get_db_url,
                maxPoolSize=10,
                minPoolSize=10)
            self.db = self.client[settings.MONGO_DB]
            logger.info("Connected to MongoDB.")


            if self.db is None:
                logger.warning("Database does not exist.")


    async def close_database_connection(self):
        logger.info("Closing connection with MongoDB.")
        if self.client:
            self.client.close()
            logger.info("Closed connection with MongoDB.")