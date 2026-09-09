from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

# backend/ folder (this file lives at backend/app/core/config.py)
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings, loaded from backend/.env when present."""

    # LLM (Ollama)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # Vector store (built by notebooks/rag_pipeline.ipynb)
    VECTOR_STORE_DIR: str = str(BASE_DIR / "data" / "vector_store")
    COLLECTION_NAME: str = "ecommerce_rag"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Retrieval
    TOP_K: int = 4

    # API
    APP_NAME: str = "RAG Assistant API"
    APP_VERSION: str = "1.0.0"
    CORS_ORIGINS: str = "http://localhost:8501"  # comma-separated list

    model_config = {
        "env_file": str(BASE_DIR / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()