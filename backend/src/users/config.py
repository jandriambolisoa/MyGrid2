import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings (BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    secret_key: str
    algorithm: str
    token_expires_minutes: int
    refresh_token_expires_minutes: int

settings = Settings()