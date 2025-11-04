from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import List
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    environment: str = "development"
    log_level: str = "INFO"

    # Paths (env는 backend 폴더 기준 상대경로 가정)
    data_dir: str = "../data"
    manuscript_dir: str = "../data/manuscripts"
    embedding_dir: str = "../data/embeddings"
    corpus_dir: str = "../data/corpus"
    report_dir: str = "../data/reports"

    # Security
    secret_key: str = "change-me"
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Limits
    max_upload_size_mb: int = 10
    allowed_extensions: List[str] = ["txt", "docx", "pdf", "md"]

    def as_abs(self, path: str) -> Path:
        base = Path(__file__).resolve().parents[2]  # backend/
        return (base / path).resolve()

    @property
    def data_path(self) -> Path:
        return self.as_abs(self.data_dir)

    @property
    def manuscript_path(self) -> Path:
        return self.as_abs(self.manuscript_dir)

    @property
    def embedding_path(self) -> Path:
        return self.as_abs(self.embedding_dir)

    @property
    def corpus_path(self) -> Path:
        return self.as_abs(self.corpus_dir)

    @property
    def report_path(self) -> Path:
        return self.as_abs(self.report_dir)

    def ensure_dirs(self) -> None:
        for p in [self.data_path, self.manuscript_path, self.embedding_path, self.corpus_path, self.report_path]:
            p.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_dirs()
