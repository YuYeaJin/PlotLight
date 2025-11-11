# app/config.py
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from pathlib import Path
from typing import List
import os, json, sys


# ---------- Base directories ----------
def _documents_dir() -> Path:
    """
    사용자의 '문서(Documents)' 폴더 경로를 결정한다.
    - OneDrive가 설정되어 있다면 OneDrive의 Documents 경로를 우선 사용.
    - 없다면 기본 사용자 홈의 Documents 경로를 사용.
    - Documents 폴더가 없을 경우 사용자 홈 폴더를 최종 폴백으로 사용.
    """
    od = os.getenv("OneDriveConsumer") or os.getenv("OneDriveCommercial")
    if od:
        od_docs = Path(od) / "Documents"
        if od_docs.exists():
            return od_docs
    docs = Path.home() / "Documents"
    return docs if docs.exists() else Path.home()


def _app_dir() -> Path:
    """
    프로그램(앱) 폴더 경로를 결정한다.
    - 패키징된 실행(예: PyInstaller)이라면 실행 파일이 있는 폴더를 반환.
    - 개발/소스 실행이라면 현재 파일 기준 두 단계 상위(보통 backend/)를 반환.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]  # backend/


USER_BASE = _documents_dir() / "PlotLight"  # 문서/PlotLight (사용자용 결과만)
APP_BASE  = _app_dir()                      # 프로그램 폴더 (시스템성 파일)


# ---------- Settings ----------
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    environment: str = "development"
    log_level: str = "INFO"

    # 사용자에게 보이는 저장소: 문서/PlotLight/원문, 리포트
    manuscript_dir: str = "원문"
    report_dir: str     = "리포트"

    # 시스템성 저장소(문서에 두지 않음) 
    log_file: str = "logs/plotlight.log"                 # APP_BASE/logs/plotlight.log
    enable_embeddings: bool = False                      # 기본: 비활성화
    persist_embeddings: bool = False                     # 기본: 저장 안 함
    embedding_dir: str = "cache/embeddings"              # APP_BASE 하위
    corpus_dir: str    = "cache/corpus"                  # APP_BASE 하위
    chroma_persist_dir: str = "cache/embeddings/chroma"  # APP_BASE 하위"

    # Security / CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Limits
    max_upload_size_mb: int = 10
    allowed_extensions: List[str] = ["txt", "docx", "pdf", "md"]

    # RAG/Embedding (자리만 유지)
    chroma_persist_dir: str = "data/embeddings/chroma"
    embedding_model: str = "BAAI/bge-small-ko-v1.5"
    embedding_dimension: int = 384
    max_embedding_tokens: int = 512
    rag_top_k: int = 5
    rag_similarity_threshold: float = 0.7
    chunk_size: int = 700
    chunk_overlap: int = 70

    # weights/workers
    default_genre_weight: float = 0.15
    default_style_weight: float = 0.25
    default_character_weight: float = 0.25
    default_plausibility_weight: float = 0.20
    default_marketability_weight: float = 0.15
    worker_count: int = 2
    max_concurrent_analyses: int = 3
    cache_ttl_seconds: int = 3600

    # ---------- Validators ----------
    @field_validator("cors_origins", mode="before")
    def _parse_cors(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return None
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
                return None
            items = json.loads(s) if s.startswith("[") else [x.strip() for x in s.split(",") if x.strip()]
        else:
            return v
        return [i.lower().lstrip(".") for i in items]

    # ---------- Path resolvers ----------
    def _user_abs(self, p: str) -> Path:
        """상대경로 → Documents/PlotLight 기준"""
        q = Path(p);  
        return q if q.is_absolute() else (USER_BASE / q).resolve()

    def _app_abs(self, p: str) -> Path:
        """상대경로 → 프로그램 폴더(APP_DIR) 기준 (로그 등 시스템성 파일)"""
        q = Path(p);  
        return q if q.is_absolute() else (APP_BASE / q).resolve()


    # 사용자 폴더 (문서/PlotLight/원문, 리포트)
    @property
    def manuscript_path(self) -> Path: return self._user_abs(self.manuscript_dir)
    @property
    def report_path(self)    -> Path: return self._user_abs(self.report_dir)

    # 시스템/로그/캐시 (프로그램 폴더 쪽)
    @property
    def log_abs_file(self)   -> Path: return self._app_abs(self.log_file)
    @property
    def log_path(self)       -> Path: return self.log_abs_file.parent
    @property
    def embedding_path(self) -> Path: return self._app_abs(self.embedding_dir)
    @property
    def corpus_path(self)    -> Path: return self._app_abs(self.corpus_dir)
    @property
    def chroma_path(self)    -> Path: return self._app_abs(self.chroma_persist_dir)


    # ---------- Ensure dirs ----------
    def ensure_dirs(self) -> None:
        # ─ 사용자 폴더(문서/PlotLight): 원문/리포트만 생성 ─
        self.manuscript_path.mkdir(parents=True, exist_ok=True)
        self.report_path.mkdir(parents=True, exist_ok=True)

        # ─ 시스템/프로그램 폴더(APP_BASE): 로그 및 (옵션) 캐시/임베딩 ─
        self.log_path.mkdir(parents=True, exist_ok=True)
        # 임베딩/코퍼스/크로마는 필요할 때만 생성
        if self.enable_embeddings:
            self.embedding_path.mkdir(parents=True, exist_ok=True)
            if self.persist_embeddings:
                self.corpus_path.mkdir(parents=True, exist_ok=True)
                self.chroma_path.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_dirs()
