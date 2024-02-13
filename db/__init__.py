from db.connection import DbConnectionManager


db_manager = DbConnectionManager()


async def get_database() -> DbConnectionManager:
    return db_manager
