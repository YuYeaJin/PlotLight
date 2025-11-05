from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import List
import os, json
from pydantic import field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # 있으면 더 유연, 없어도 필드 다 정의했으면 OK
    )

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
    log_file: str = "../logs/plotlight.log"  # ★ 추가

    # Security
    secret_key: str = "change-me"
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Limits
    max_upload_size_mb: int = 10
    allowed_extensions: List[str] = ["txt", "docx", "pdf", "md"]

    # ★ 추가: 벡터/RAG/워커 관련 (에러에 나온 키들 전부)
    chroma_persist_dir: str = "../data/embeddings/chroma"
    embedding_model: str = "BAAI/bge-small-ko-v1.5"
    embedding_dimension: int = 384
    max_embedding_tokens: int = 512
    rag_top_k: int = 5
    rag_similarity_threshold: float = 0.7
    chunk_size: int = 700
    chunk_overlap: int = 70

    default_genre_weight: float = 0.15
    default_style_weight: float = 0.25
    default_character_weight: float = 0.25
    default_plausibility_weight: float = 0.20
    default_marketability_weight: float = 0.15

    worker_count: int = 2
    max_concurrent_analyses: int = 3
    cache_ttl_seconds: int = 3600

    # ▼ .env가 콤마/JSON/빈값이어도 수용 (선택이지만 권장)
    @field_validator("cors_origins", mode="before")
    def _parse_cors(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return None  # -> 기본값 사용
            if s == "*":
                return ["*"]
            if s.startswith("["):
                return json.loads(s)
            return [x.strip() for x in s.split(",") if x.strip()]
        return v

    @field_validator("allowed_extensions", mode="before")
    def _parse_exts(cls, v):
        if isinstance(v, list):
            items = v
        elif isinstance(v, str):
            s = v.strip()
            if not s:
                return None  # -> 기본값 사용
            if s.startswith("["):
                items = json.loads(s)
            else:
                items = [x.strip() for x in s.split(",") if x.strip()]
        else:
            return v
        return [i.lower().lstrip(".") for i in items]

    def as_abs(self, path: str) -> Path:
        base = Path(__file__).resolve().parents[2]  # backend/
        return (base / path).resolve()

    @property
    def data_path(self) -> Path: return self.as_abs(self.data_dir)
    @property
    def manuscript_path(self) -> Path: return self.as_abs(self.manuscript_dir)
    @property
    def embedding_path(self) -> Path: return self.as_abs(self.embedding_dir)
    @property
    def corpus_path(self) -> Path: return self.as_abs(self.corpus_dir)
    @property
    def report_path(self) -> Path: return self.as_abs(self.report_dir)
    @property
    def chroma_path(self) -> Path: return self.as_abs(self.chroma_persist_dir)   # ★ 추가
    @property
    def log_path(self) -> Path: return self.as_abs(self.log_file).parent        # ★ 추가

    def ensure_dirs(self) -> None:
        for p in [
            self.data_path, self.manuscript_path, self.embedding_path,
            self.corpus_path, self.report_path, self.chroma_path, self.log_path # ★ 로그/Chroma 폴더 생성
        ]:
            p.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_dirs()
