import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings (BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    debug: int = 0

    # Security related settings
    secret_key: str
    algorithm: str
    token_expires_minutes: int
    refresh_token_expires_minutes: int

    # Redirections related settings
    website_url: str
    confirmed_email_url: str

    # Microservices related settings
    ms_mailings_url: str

settings = Settings()