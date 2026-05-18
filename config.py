from dataclasses import dataclass
import dotenv
import os


dotenv.load_dotenv()

# config class for db
@dataclass
class DatabaseConfig:
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

# api config class
@dataclass
class APIConfig:
    API_KEY: str = os.getenv("API_KEY")

# config for drf project
@dataclass
class APPConfig:
    THROTTLE_RATE: str = os.getenv("THROTTLE_RATE")
    PAGE_SIZE: int = os.getenv("PAGE_SIZE")