# app/routes/files.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..config import settings
from ..models.schemas import AnalyzeRunResponse, SectionScore, Metric, EvidenceItem
import hashlib

router = APIRouter(prefix="/files", tags=["files"])

def _check_size(n_bytes: int):
    limit = settings.max_upload_size_mb * 1024 * 1024
    if n_bytes > limit:
        raise HTTPException(status_code=413, detail=f"File too large (>{settings.max_upload_size_mb} MB)")

def _check_ext(filename: str):
    # 확장자 검사 (없으면 통과)
    if "." in filename:
        ext = filename.rsplit(".", 1)[-1].lower().lstrip(".")
        if settings.allowed_extensions and ext not in settings.allowed_extensions:
            raise HTTPException(status_code=400, detail=f"Extension .{ext} is not allowed")

@router.post("/analyze/quick", response_model=AnalyzeRunResponse, summary="Analyze without saving")
async def analyze_quick(file: UploadFile = File(...)):
    # 1) 기본 검증
    _check_ext(file.filename or "")
    data = await file.read()  # 디스크에 저장하지 않음 (메모리에서 처리)
    _check_size(len(data))

    # 2) bytes -> text (MVP: utf-8)
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to decode file as UTF-8 text")

    # 3) 재현용 임시 ID
    content_hash = hashlib.sha256(data).hexdigest()[:16]
    manuscript_id = f"mem-{content_hash}"

    # 4) (지금은 목업 응답)
    genre = SectionScore(
        label="genre",
        score=78.0,
        metrics=[
            Metric(name="장르 확률-로맨스", value=0.62),
            Metric(name="장르 확률-판타지", value=0.28),
        ],
        evidences=[EvidenceItem(source_id="guide_romance", snippet="초반 갈등 제시", score=0.83)],
    )
    style = SectionScore(
        label="style",
        score=72.0,
        metrics=[
            Metric(name="평균 문장 길이", value=13.4, unit="어절", zscore=0.6),
            Metric(name="대사 비율", value=41.0, unit="%"),
            Metric(name="어휘 다양도", value=0.47),
        ],
    )

    return AnalyzeRunResponse(
        manuscript_id=manuscript_id,
        title=file.filename or "(업로드)",
        total_score=72.8,
        strengths=["초반 갈등 명확", "대사 비율이 장르 평균과 근접"],
        improvements=["3~5화 동기 보강 필요", "조연 말투 차별성 약함"],
        sections=[genre, style],
    )
