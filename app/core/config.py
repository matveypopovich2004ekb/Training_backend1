import os
from dataclasses import dataclass

from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: list[str]


def get_settings() -> Settings:

    db_url = os.getenv("DATABASE_URL")
    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="DB URL is not found"
        )

    cors_origins = os.getenv("CORS_ORIGINS")
    if cors_origins is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CORS URL is not found"
        )
    return Settings(
        database_url=db_url,
        cors_origins=cors_origins.split(","),
    )
