
from db import db_manager

async def startup_event():
    await db_manager.connect_to_database()

async def shutdown_event():
    await db_manager.close_database_connection()