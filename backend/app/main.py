from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import files

from .models.schemas import AnalyzeRunRequest, AnalyzeRunResponse, SectionScore, Metric, EvidenceItem

app = FastAPI(title="PlotLight API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "manuscript_path": str(settings.manuscript_path),
        "report_path": str(settings.report_path),
        "log_path": str(settings.log_path),
    }

# 업로드 라우터 등록
app.include_router(files.router)

@app.post("/analyze/run", response_model=AnalyzeRunResponse)
def analyze_run(req: AnalyzeRunRequest):
    # MVP 목업
    genre = SectionScore(label="genre", score=78.0,
        metrics=[Metric(name="장르 확률-로맨스", value=0.62), Metric(name="장르 확률-판타지", value=0.28)],
        evidences=[EvidenceItem(source_id="guide_romance", snippet="초반 갈등 제시", score=0.83)]
    )
    style = SectionScore(label="style", score=72.0,
        metrics=[Metric(name="평균 문장 길이", value=13.4, unit="어절", zscore=0.6),
                 Metric(name="대사 비율", value=41.0, unit="%"),
                 Metric(name="어휘 다양도", value=0.47)]
    )
    return AnalyzeRunResponse(
        manuscript_id=req.manuscript_id,
        title="(MVP) 샘플 원고",
        total_score=72.8,
        strengths=["초반 갈등 명확", "대사 비율이 장르 평균과 근접"],
        improvements=["3~5화 동기 보강 필요", "조연 말투 차별성 약함"],
        sections=[genre, style]
    )

# 개발 실행: uvicorn app.main:app --reload --port 8000
