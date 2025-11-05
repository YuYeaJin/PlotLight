from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from typing import Dict
from pathlib import Path
import time, re

from . import __init__  # 패키지 인식용 (없으면 무시)
from ..config import settings
from ..models.schemas import FileUploadResponse

router = APIRouter(prefix="/files", tags=["files"])

CHUNK_SIZE = 1024 * 1024  # 1MB

def _secure_filename(name: str) -> str:
    # 경로 분리 & 위험 문자 제거
    name = Path(name).name
    name = re.sub(r'[^A-Za-z0-9._-]+', "_", name)
    return name

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)) -> FileUploadResponse:
    # 확장자 검증
    ext = Path(file.filename).suffix.lower().lstrip(".")
    if ext not in [e.lower().lstrip(".") for e in settings.allowed_extensions]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"허용되지 않은 확장자입니다: .{ext} (allowed: {settings.allowed_extensions})"
        )

    # 저장 경로 준비
    settings.ensure_dirs()  # 혹시 몰라 재보장
    safe_name = _secure_filename(file.filename)
    ts = int(time.time())
    target_name = f"{ts}_{safe_name}"
    target_path = settings.manuscript_path / target_name

    # 용량 제한 + 스트리밍 저장
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    written = 0
    try:
        with open(target_path, "wb") as f:
            while True:
                chunk = await file.read(CHUNK_SIZE)
                if not chunk:
                    break
                written += len(chunk)
                if written > max_bytes:
                    try:
                        target_path.unlink(missing_ok=True)
                    except Exception:
                        pass
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"파일이 너무 큽니다. 최대 {settings.max_upload_size_mb}MB"
                    )
                f.write(chunk)
    finally:
        await file.close()

    # 간단한 아이디(파일명 기반) 반환
    manuscript_id = target_name.rsplit(".", 1)[0]
    return {
        "manuscript_id": manuscript_id,
        "filename": safe_name,
        "size_bytes": written,
        "saved_as": target_name,
        "saved_dir": str(settings.manuscript_path),
        "ext": ext,
    }
