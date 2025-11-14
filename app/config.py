"""Application configuration and settings."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/stackmason"
    )
    
    # Environment
    APP_ENV: str = os.getenv("APP_ENV", "local")
    IS_LOCAL: bool = APP_ENV == "local"
    
    # API Metadata
    APP_TITLE: str = "StackMason CloudFormation API"
    APP_DESCRIPTION: str = "GraphQL API for CloudFormation resources, properties, and regions"
    APP_VERSION: str = "1.0.0"
    
    # CORS
    CORS_ORIGINS: list = ["*"]  # In production, replace with specific origins
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]


settings = Settings()

