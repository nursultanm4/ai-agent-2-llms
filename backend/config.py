import os
from dotenv import load_dotenv
from typing import List


load_dotenv()


class Settings:

    # API Configuration
    API_TITLE: str = "AI Agent Backend"
    API_DESCRIPTION: str = "Orchestrates LLM calls for user queries using Gemma model and gpt-4o-mini as an executor"
    API_VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    
    # HTTP Configuration
    HTTP_REQUEST_TIMEOUT_S: int = int(os.getenv("HTTP_REQUEST_TIMEOUT_S", 30))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", 2))
    
    # Cache Configuration
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", 600))
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", 1000))
    
    # LLM Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMMA_ORCHESTRATOR_MODEL: str = os.getenv("GEMMA_ORCHESTRATOR_MODEL", "gemma-3-1b-it")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_EXECUTOR_MODEL: str = os.getenv("OPENAI_EXECUTOR_MODEL", "gpt-4o-mini")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    LOG_FILE: str = os.getenv("LOG_FILE", "ai_agent.log")
    LOG_MAX_SIZE: int = int(os.getenv("LOG_MAX_SIZE", 10 * 1024 * 1024))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", 5))

# Global settings instance
settings = Settings()


