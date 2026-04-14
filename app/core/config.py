from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: list[str]


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL"),
        cors_origins=os.getenv("CORS_ORIGINS", "").split(',')
    )








