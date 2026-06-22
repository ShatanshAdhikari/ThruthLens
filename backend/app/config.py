from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    TAVILY_API_KEY: Optional[str] = None
    GOOGLE_FACT_CHECK_API_KEY: Optional[str] = None
    
    # Model Settings
    OLLAMA_MODEL: str = "llama3"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VERIFIER_MODEL: str = "cross-encoder/nli-deberta-v3-small"
    
    # Database Settings
    CHROMA_PERSIST_DIR: str = "db/chroma"
    
    # Retrieval & Consensus Settings
    USE_WEB_SEARCH: bool = True
    MAX_SEARCH_RESULTS_PER_SOURCE: int = 5
    CONSENSUS_THRESHOLD: float = 0.7
    MIN_SOURCES_FOR_CONSENSUS: int = 3
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
