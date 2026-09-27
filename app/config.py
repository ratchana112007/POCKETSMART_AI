import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "dev-secret-change-me"
    )

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./pocketsmart.db"
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    debug: bool = os.getenv(
        "DEBUG",
        "True"
    ).lower() in {
        "1",
        "true",
        "yes",
        "on"
    }


settings = Settings()