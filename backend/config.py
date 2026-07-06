"""
RESEARCHMINDAI - Configuration Module
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # AI API Keys
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    groq_api_key: str = Field(default="", env="GROQ_API_KEY")
    tavily_api_key: str = Field(default="", env="TAVILY_API_KEY")

    # LLM Config
    default_llm: str = Field(default="gemini", env="DEFAULT_LLM")
    gemini_model: str = Field(default="gemini-1.5-pro", env="GEMINI_MODEL")
    groq_model: str = Field(default="llama-3.3-70b-versatile", env="GROQ_MODEL")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", env="EMBEDDING_MODEL")

    # Database
    sqlite_db_path: str = Field(default="./data/researchmind.db", env="SQLITE_DB_PATH")
    chroma_persist_dir: str = Field(default="./data/chroma", env="CHROMA_PERSIST_DIR")

    # Storage
    upload_dir: str = Field(default="./data/uploads", env="UPLOAD_DIR")
    reports_dir: str = Field(default="./data/reports", env="REPORTS_DIR")

    # Research Config
    max_research_depth: int = Field(default=5, env="MAX_RESEARCH_DEPTH")
    max_search_results: int = Field(default=10, env="MAX_SEARCH_RESULTS")
    max_wiki_results: int = Field(default=5, env="MAX_WIKI_RESULTS")

    # Server
    backend_host: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    backend_port: int = Field(default=8000, env="BACKEND_PORT")
    cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        env="CORS_ORIGINS"
    )

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    def ensure_dirs(self):
        """Create required data directories if they don't exist."""
        for path in [
            self.upload_dir,
            self.reports_dir,
            self.chroma_persist_dir,
            Path(self.sqlite_db_path).parent,
        ]:
            Path(path).mkdir(parents=True, exist_ok=True)


settings = Settings()
