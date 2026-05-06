"""Configuration management using Pydantic Settings"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    APP_NAME: str = "AI Education Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_education"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LLM Services
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536
    
    # Vector Database
    VECTOR_STORE_TYPE: str = "pgvector"
    
    # File Storage
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "ai-education"
    
    # CORS
    CORS_ORIGINS: str = '["http://localhost:3000","http://localhost:8501"]'
    
    # LMS Integration
    LMS_TYPE: str = "google_classroom"
    LMS_CLIENT_ID: str = ""
    LMS_CLIENT_SECRET: str = ""
    
    # Curriculum
    DSE_CURRICULUM_PATH: str = "./data/curriculum/dse.yaml"
    TSA_CURRICULUM_PATH: str = "./data/curriculum/tsa.yaml"
    
    # RAG Configuration
    RAG_TOP_K: int = 10
    RAG_CHUNK_SIZE: int = 500
    RAG_CHUNK_OVERLAP: int = 50
    
    @property
    def is_production(self) -> bool:
        return not self.DEBUG
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS from string"""
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["http://localhost:3000"]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()