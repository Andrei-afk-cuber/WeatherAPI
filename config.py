from dataclasses import dataclass
import dotenv
import os


dotenv.load_dotenv()

@dataclass
class Config:
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")