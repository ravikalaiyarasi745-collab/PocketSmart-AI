import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "PocketSmart AI")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://127.0.0.1:8000")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./pocketsmart.db",
    )

    @property
    def cors_origin_list(self):
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


def get_settings() -> Settings:
    return Settings()