# PlotLight

<div align="center">
  <h3>웹소설 원고 자동 평가 데스크톱 애플리케이션</h3>
  <p>AI 기반 장르 분석, 시장성 평가, 개연성 검증을 제공하는 작가 도구</p>
</div>

---

## 📖 개요

PlotLight는 웹소설 작가를 위한 원고 분석 데스크톱 애플리케이션입니다.  
현재는 **규칙 기반 분석**으로 동작하며, 향후 **AI 기반 장르/시장성/개연성 평가**로 확장될 예정입니다.

### ✨ 주요 기능

#### 현재 구현
- **문체 분석**: 문장 길이, 문단 수, 대사 비율 등 정량적 지표 제공
- **장르 판별 (초기)**: 키워드 기반 장르 추정

#### 개발 예정
- **고급 장르 판별**: 제로샷 분류 모델 기반 정교한 장르 식별
- **캐릭터 분석**: 발화 패턴, 말투 차별성, 등장 비율
- **개연성 검증**: 사건-동기-결과 구조 및 인과관계 흐름 평가
- **시장성 평가**: RAG 기반 장르별 트렌드·가이드 비교 분석
- **리포트 생성**: PDF/DOCX 형식의 상세 분석 리포트

---

## 🛠️ 기술 스택

### Backend
- FastAPI (Python 3.10+)
- Pydantic v2
- Uvicorn
- *(예정)* Sentence Transformers, ChromaDB, WeasyPrint

### Frontend
- React 18 + TypeScript
- Vite
- Electron
- *(예정)* Recharts 등 데이터 시각화

---

## 🚀 설치 및 실행

### 사전 요구사항
- Python 3.10 이상
- Node.js 18 이상
- *(향후 AI 기능 사용 시)* 최소 8GB RAM 권장

### 1. 저장소 클론
```bash
git clone https://github.com/YuYeaJin/PlotLight.git
cd PlotLight
```

### 2. 백엔드 설정
```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

**환경 변수 설정** (선택)
```bash
# .env.example이 있다면 복사
cp .env.example .env
# 필요한 설정 값 입력 (저장 경로, CORS 등)
```

**백엔드 실행**
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- 헬스 체크: http://localhost:8000/health
- API 문서: http://localhost:8000/docs

### 3. 프론트엔드 설정
```bash
cd frontend
npm install
```

**환경 변수 설정**
```bash
# frontend/.env 또는 .env.development
VITE_API_BASE=http://127.0.0.1:8000
```

### 4. 개발 모드 실행
```bash
# 터미널 1: 백엔드
cd backend
uvicorn app.main:app --reload

# 터미널 2: 프론트엔드 (브라우저)
cd frontend
npm run dev

# 터미널 3: Electron (데스크톱 앱)
cd frontend
npm run electron:dev
```

### 5. 프로덕션 빌드
```bash
cd frontend
npm run build
npm run electron:build
```

---

## 📁 프로젝트 구조

```
PlotLight/
├── backend/              # FastAPI 서버 및 분석 엔진
│   ├── app/
│   │   ├── main.py       # FastAPI 엔트리포인트
│   │   ├── routes/       # 엔드포인트 정의
│   │   ├── models/       # Pydantic 스키마
│   │   ├── services/     # 분석 로직
│   │   └── config.py     # 설정/경로 관리
│   └── requirements.txt
├── frontend/             # React UI 및 Electron
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/        # QuickAnalyze 등
│   │   ├── components/
│   │   └── styles/
│   └── package.json
└── README.md
```

---

## 📡 API 문서

서버 실행 후 **http://localhost:8000/docs** 에서 Swagger UI로 전체 API 확인 가능

### 현재 주요 엔드포인트

#### `GET /health`
서버 상태 확인

#### `POST /files/analyze/quick`
원고 업로드 및 규칙 기반 빠른 분석
- **multipart/form-data**:
  - `file`: 원고 파일
  - `persist`: (선택) 원고 파일 저장 여부
  - `save_report`: (선택) 분석 결과 JSON 저장 여부

#### `POST /analyze/run`
초기 목업용 분석 엔드포인트 (테스트용)

### 예정 엔드포인트
- `POST /api/manuscripts/upload`: 원고 업로드
- `POST /api/manuscripts/analyze`: 전체 분석 실행
- `POST /api/rag/query`: RAG 검색
- `POST /api/reports/generate`: 리포트 생성

---

## 🗓️ 개발 로드맵

### MVP (현재)
- [x] 프로젝트 구조 설계
- [x] 기본 업로드 및 전처리
- [x] 규칙 기반 분석 파이프라인
- [x] 간단한 UI (원고 업로드 & 결과 표시)
- [ ] 리포트 JSON 저장 옵션 고도화
- [ ] 기본 설정 UI (테마, 저장 옵션 등)

### v1.0
- [ ] LLM 기반 장르 판별 파이프라인
- [ ] 시장성·개연성 1차 평가 로직
- [ ] PDF/DOCX 리포트 생성
- [ ] 배치 분석 (여러 원고 동시 처리)
- [ ] 결과 비교 기능

### v2.0
- [ ] LangGraph 통합 (분기/병렬/체크포인트)
- [ ] RAG 서비스 구현
- [ ] 휴먼 피드백 루프
- [ ] 고급 시각화

---

## 🗂️ 데이터팩 관리 *(예정)*

PlotLight는 향후 RAG 기반 평가를 위해 자체 제작 가이드 데이터팩을 사용할 예정입니다.

### 데이터팩 형식 (초안)
```
data/corpus/2025Q4_romance_fantasy/
├── metadata.json
├── guides/
│   ├── hooks.md
│   ├── tropes.md
│   └── taboos.md
└── embeddings/
```

### 데이터팩 인덱싱 (예정 API 예시)
```bash
curl -X POST http://localhost:8000/api/rag/ingest-datapack \
  -H "Content-Type: application/json" \
  -d '{"datapack_path": "data/corpus/2025Q4_romance_fantasy"}'
```

---

## 🤝 기여 가이드

1. 이슈 생성 또는 기존 이슈 확인
2. 기능 브랜치 생성 (`feature/amazing-feature`)
3. 커밋 (`git commit -m 'Add amazing feature'`)
4. 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

---

## 📧 연락처

**프로젝트 관리자**: 유예진  
**이메일**: yyj9290@naver.com  
**GitHub**: https://github.com/YuYeaJin/PlotLight

---

## 🙏 감사의 말

- [FastAPI](https://fastapi.tiangolo.com/) 및 Python 생태계
- [React](https://react.dev/) & [Electron](https://www.electronjs.org/) 커뮤니티
- *(예정)* Sentence Transformers, ChromaDB 등 오픈소스 프로젝트

---
