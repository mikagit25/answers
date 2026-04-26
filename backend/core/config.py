from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/answers_db"
    REDIS_URL: str = "redis://localhost:6379"
    QWEN_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # RAG Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 50
    TOP_K_RETRIEVAL: int = 5
    
    # Cache Configuration
    CACHE_TTL: int = 86400  # 24 hours in seconds
    
    class Config:
        env_file = ".env"

settings = Settings()
