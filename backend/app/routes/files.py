from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..config import settings
from ..models.schemas import AnalyzeRunResponse, SectionScore, Metric, EvidenceItem
from ..services.preprocess import extract_text_from_upload
from ..services.analysis import rule_based_analyze

import os, json, time, re, unicodedata, hashlib
from datetime import datetime
from typing import Tuple

router = APIRouter(prefix="/files", tags=["files"])

# Windows 예약/제어 문자 제거용
_INVALID = re.compile(r'[<>:"/\\|?*\x00-\x1F]')

def _check_size(n_bytes: int):
    limit = settings.max_upload_size_mb * 1024 * 1024
    if n_bytes > limit:
        raise HTTPException(status_code=413, detail=f"File too large (>{settings.max_upload_size_mb} MB)")

def _check_ext(filename: str):
    # 확장자 검사 (없으면 통과)
    if filename and "." in filename:
        ext = filename.rsplit(".", 1)[-1].lower().lstrip(".")
        if settings.allowed_extensions and ext not in settings.allowed_extensions:
            raise HTTPException(status_code=400, detail=f"Extension .{ext} is not allowed")

def sanitize_filename(name: str) -> str:
    # 양끝 공백/점 제거, 제어문자 제거
    name = unicodedata.normalize("NFC", name).strip().strip(".")
    name = _INVALID.sub("_", name)
    # 너무 긴 이름 제한 (NTFS는 255바이트 제한: 여유있게 120자로)
    return name[:120] or "untitled"


def build_storage_name(original: str, content_bytes: bytes) -> Tuple[str, str]:
    """
    저장용 파일명과(타임스탬프+원본명) 충돌 방지용 짧은 해시를 반환
    """
    if "." in (original or ""):
        base, ext = original.rsplit(".", 1)
        ext = ext.lower()
    else:
        base, ext = (original or "upload"), "txt"
    base = sanitize_filename(base)
    ts = datetime.now().strftime("%y.%m.%d")
    fname = f"{ts}_{base}.{ext}"
    short = hashlib.sha1(content_bytes).hexdigest()[:6]
    return fname, short

@router.post("/analyze/quick", response_model=AnalyzeRunResponse, summary="Analyze without saving")
async def analyze_quick(
    file: UploadFile = File(...),
    persist: bool = Form(False),      # 저장 여부 (기본: 미저장)
    save_report: bool = Form(False),  # 리포트 저장 여부
):
    # 1) 기본 검증
    _check_ext(file.filename or "")
    contents = await file.read()  # 디스크에 저장하지 않음(옵션)
    _check_size(len(contents))

    started = time.perf_counter()

    # 2) 텍스트 추출 (메모리에서)
    try:
        text = await extract_text_from_upload(filename=file.filename or "", data=contents)
    except Exception as e:
        # 텍스트 추출 실패는 400으로 돌려서 프론트에서 메세지 확인 가능하게
        raise HTTPException(status_code=400, detail=f"텍스트 추출 실패: {e}")

    # 3) 규칙 기반 분석 (하드코딩 로직)
    result = rule_based_analyze(text)

    # 4) 원문/리포트 저장 준비
    stored_filename: str | None = None

    # 내용 해시 + 타임스탬프로 사람이 보기 좋은 ID 하나는 항상 만들어 둔다
    content_hash = hashlib.sha1(contents).hexdigest()[:10]
    manuscript_id = f"{content_hash}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # 4-1) 원문 저장 (persist가 true일 때만)
    if persist:
        os.makedirs(settings.manuscript_path, exist_ok=True)

        # 원본 파일명을 바탕으로 저장용 파일명 생성
        fname, short = build_storage_name(file.filename or "upload", contents)
        fullpath = os.path.join(settings.manuscript_path, fname)

        # 파일명이 이미 존재하면 짧은 해시 꼬리표 추가
        if os.path.exists(fullpath):
            if "." in fname:
                stem, ext = fname.rsplit(".", 1)
                fname = f"{stem}_{short}.{ext}"
            else:
                fname = f"{fname}_{short}"
            fullpath = os.path.join(settings.manuscript_path, fname)

        with open(fullpath, "wb") as f:
            f.write(contents)

        stored_filename = fname

    elapsed_ms = int((time.perf_counter() - started) * 1000)

    # 5) 응답용 섹션 구성 (하드코딩/규칙 기반)
    genre = SectionScore(
        label="genre",
        score=result["scores"]["genre"],
        metrics=[
            Metric(name="문장 수", value=result["stats"]["num_sentences"]),
            # Metric(name="추정 장르", value=None, note=result.get("genre_label")),
        ],
        evidences=[
            EvidenceItem(source_id="rule", snippet="키워드 기반 장르 추정", score=0.7)
        ],
    )

    style = SectionScore(
        label="style",
        score=result["scores"]["style"],
        metrics=[
            Metric(name="평균 문장 길이", value=result["stats"]["avg_sentence_len"]),
            Metric(name="문단 수", value=result["stats"]["num_paragraphs"]),
        ],
        evidences=[
            EvidenceItem(
                source_id="rule",
                snippet="문장 길이/문단 수 기반 스타일 점수",
                score=0.8,
            )
        ],
    )

    character = SectionScore(
        label="character",
        score=result["scores"]["character"],
        metrics=[
            Metric(name="대사 비율", value=result["stats"]["quote_ratio"]),
        ],
        evidences=[
            EvidenceItem(
                source_id="rule",
                snippet="대사 비율을 캐릭터성에 반영",
                score=0.6,
            )
        ],
    )

    market = SectionScore(
        label="market",
        score=result["scores"]["marketability"],
        metrics=[],
        evidences=[
            EvidenceItem(
                source_id="rule",
                snippet="AI 연동 전 임시 시장성 점수",
                score=0.3,
            )
        ],
    )

    plaus = SectionScore(
        label="causality",
        score=result["scores"]["plausibility"],
        metrics=[],
        evidences=[
            EvidenceItem(
                source_id="rule",
                snippet="AI 연동 전 임시 개연성 점수",
                score=0.3,
            )
        ],
    )

    # 6) 응답 객체 생성
    resp = AnalyzeRunResponse(
        total_score=result["scores"]["total"],
        strengths=result["strengths"],
        improvements=result["improvements"],
        sections=[genre, style, character, market, plaus],
        manuscript_id=manuscript_id,
        analyzed_at=datetime.now(),
        processing_ms=elapsed_ms,
        title=(file.filename or "(업로드)"),
    )

    # 7) 리포트 JSON 저장 (save_report가 true면, persist 여부와 상관 없이)
    if save_report:
        os.makedirs(settings.report_path, exist_ok=True)
        report_data = resp.model_dump()
        with open(
            os.path.join(settings.report_path, f"{manuscript_id}.json"),
            "w",
            encoding="utf-8",
        ) as jf:
            json.dump(report_data, jf, ensure_ascii=False, indent=2)

    # 8) 클라이언트로 응답 반환
    return resp

# @router.post("/analyze/quick", response_model=AnalyzeRunResponse, summary="Analyze with optional persist")
# async def analyze_quick(
#     file: UploadFile = File(...),
#     persist: bool = Form(False),      # 저장 여부 (기본: 미저장)
#     save_report: bool = Form(False),  # 리포트 저장 여부 (persist=True일 때만 의미)
# ):
#     # 1) 기본 검증
#     _check_ext(file.filename or "")
#     contents = await file.read()  # 디스크에 저장하지 않음(옵션)
#     _check_size(len(contents))

#     started = time.perf_counter()

#     # 2) 텍스트 추출 (메모리에서)
#     try:
#         text = await extract_text_from_upload(filename=file.filename or "", data=contents)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"텍스트 추출 실패: {e}")

#     # 3) 규칙 기반 분석
#     result = rule_based_analyze(text)

#     # 4) 필요 시만 저장
#     manuscript_id = None
#     stored_filename = None
#     if persist:
#         os.makedirs(settings.manuscript_path, exist_ok=True)

#         fname, short = build_storage_name(file.filename or "upload", contents)
#         fullpath = os.path.join(settings.manuscript_path, fname)

#         # 파일명이 이미 존재하면 짧은 해시 꼬리표 추가
#         if os.path.exists(fullpath):
#             if "." in fname:
#                 stem, ext = fname.rsplit(".", 1)
#                 fname = f"{stem}_{short}.{ext}"
#             else:
#                 fname = f"{fname}_{short}"
#             fullpath = os.path.join(settings.manuscript_path, fname)

#         with open(fullpath, "wb") as f:
#             f.write(contents)

#         stored_filename = fname
#         # 사람이 보기 좋게: 내용 해시 + 타임스탬프
#         content_hash = hashlib.sha1(contents).hexdigest()[:10]
#         manuscript_id = f"{content_hash}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

#         if save_report:
#             os.makedirs(settings.report_path, exist_ok=True)
#             report_json = {
#                 "manuscript_id": manuscript_id,
#                 "original_filename": file.filename,
#                 "stored_filename": stored_filename,
#                 "analyzed_at": datetime.now().isoformat(),
#                 "result": result,
#             }
#             with open(
#                 os.path.join(settings.report_path, f"{manuscript_id}.json"),
#                 "w", encoding="utf-8"
#             ) as jf:
#                 json.dump(report_json, jf, ensure_ascii=False, indent=2)

#     elapsed_ms = int((time.perf_counter() - started) * 1000)


#     # 5) 스키마에 맞게 응답 구성
#     genre = SectionScore(
#         label="genre",
#         score=result["scores"]["genre"],
#         metrics=[
#             Metric(name="문장 수", value=result["stats"]["num_sentences"]),
#             Metric(name="대사 비율", value=result["stats"]["quote_ratio"]),
#         ],
#         evidences=[EvidenceItem(source_id="rule", snippet="규칙 기반 통계 산출", score=1.0)],
#     )
#     style = SectionScore(
#         label="style",
#         score=result["scores"]["style"],
#         metrics=[
#             Metric(name="평균 문장 길이", value=result["stats"]["avg_sentence_len"]),
#             Metric(name="문단 수", value=result["stats"]["num_paragraphs"]),
#         ],
#         evidences=[EvidenceItem(source_id="rule", snippet="규칙 기반 통계 산출", score=1.0)],
#     )

#     return AnalyzeRunResponse(
#         total_score=result["scores"]["total"],
#         strengths=result["strengths"],
#         improvements=result["improvements"],
#         sections=[genre, style],
#         manuscript_id=manuscript_id,             # persist=False면 None
#         # ↓ 아래 3개 필드는 스키마에 없다면 빼세요.
#         analyzed_at=datetime.now().isoformat(),
#         processing_ms=elapsed_ms,
#         persisted=persist,
#         # 선택: 스키마에 title 있으면 채우기
#         title=(file.filename or "(업로드)"),
#     )