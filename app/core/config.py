from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Definitions
    PROJECT_NAME: str = "Architect Agent MVP"
    VERSION: str = "1.0.0"

    # Supabase Integration
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # Supported LLM Providers
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    NVIDIA_API_KEY: str = ""
    HF_TOKEN: str = ""

    # Token constraints/Config
    LOG_LEVEL: str = "INFO"
    MAX_TOKEN_BUDGET: int = 500000

    class Config:
        env_file = ".env"


settings = Settings()
