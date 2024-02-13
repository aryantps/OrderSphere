from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from enum import Enum

load_dotenv()



class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Settings(BaseSettings):
    HOST:str
    PORT:str

    log_level : LogLevel = LogLevel.INFO

    # MongoDB configurations
    MONGO_USERNAME:str
    MONGO_PASSWORD:str
    MONGO_HOST:str
    MONGO_PORT:int
    MONGO_DB:str 
    MONGO_REMOTE_URL:str 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def get_db_url(self):
        # return f"mongodb+srv://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
        return f"mongodb+srv://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_REMOTE_URL}"

settings = Settings()