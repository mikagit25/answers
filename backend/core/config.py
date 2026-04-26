from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/answers_db"
    REDIS_URL: str = "redis://localhost:6379"
    
    # LLM Providers Configuration (Multiple providers with fallback)
    # Priority order: GROQ -> OPENROUTER -> OLLAMA (local) -> HUGGINGFACE
    
    # Groq (Free tier: 30 requests/min, 200 requests/day)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"  # Free model on Groq
    
    # OpenRouter (Free models available)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "meta-llama/llama-3-8b-instruct:free"  # Free tier
    
    # Ollama (Local, completely free)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"  # Local model
    
    # Hugging Face Inference API (Free tier)
    HUGGINGFACE_API_KEY: str = ""
    HUGGINGFACE_MODEL: str = "HuggingFaceH4/zephyr-7b-beta"
    
    # Fallback Configuration
    LLM_PROVIDER_PRIORITY: List[str] = ["groq", "openrouter", "ollama", "huggingface"]
    MAX_RETRIES_PER_PROVIDER: int = 3
    REQUEST_TIMEOUT: int = 30  # seconds
    
    # RAG Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 50
    TOP_K_RETRIEVAL: int = 5
    
    # Cache Configuration
    CACHE_TTL: int = 86400  # 24 hours in seconds
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields from .env

settings = Settings()
