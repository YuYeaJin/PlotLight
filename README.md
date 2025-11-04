# PlotLight

웹소설 원고 자동 평가 데스크톱 애플리케이션

## 개요

PlotLight는 웹소설 원고를 다각도로 분석하여 객관적인 피드백을 제공하는 AI 기반 평가 도구입니다.

### 주요 기능

- **장르 판별**: 제로샷 분류로 원고의 장르 자동 식별
- **문체 분석**: 문장 길이, 대사 비율, 어휘 다양도 등 정량적 지표 제공
- **캐릭터 분석**: 캐릭터별 발화 패턴 일관성 및 차별성 평가
- **개연성 검증**: 사건-동기-결과 구조 분석
- **시장성 평가**: RAG 기반 장르별 트렌드 가이드 참조
- **리포트 생성**: PDF/DOCX 형식의 상세 분석 리포트 출력

### 기술 스택

**Backend**
- FastAPI (Python 3.10+)
- Sentence Transformers (임베딩)
- ChromaDB (벡터 데이터베이스)
- WeasyPrint (PDF 생성)

**Frontend**
- React 18 + TypeScript
- Vite (빌드 도구)
- Electron (데스크톱 패키징)
- Recharts (데이터 시각화)

## 설치 및 실행

### 사전 요구사항

- Python 3.10 이상
- Node.js 18 이상
- 최소 8GB RAM (임베딩 모델 로드용)

### 백엔드 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 설정 입력
```

### 백엔드 실행

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 프론트엔드 설정

```bash
cd frontend
npm install
```

### 개발 모드 실행

```bash
# 터미널 1: 백엔드
cd backend
uvicorn app.main:app --reload

# 터미널 2: 프론트엔드
cd frontend
npm run dev

# 터미널 3: Electron
cd frontend
npm run electron:dev
```

### 프로덕션 빌드

```bash
cd frontend
npm run build
npm run electron:build
```

## 프로젝트 구조

```
plotlight/
├── backend/          # FastAPI 서버 및 분석 엔진
├── frontend/         # React UI 및 Electron 래퍼
├── data/            # 로컬 데이터 저장소
└── docs/            # 문서
```

자세한 내용은 [Architecture 문서](docs/architecture.md)를 참조하세요.

## 데이터팩 관리

PlotLight는 저작권 보호를 위해 자체 제작한 가이드 데이터팩을 사용합니다.

### 데이터팩 형식

```
data/corpus/2025Q4_romance_fantasy/
├── metadata.json
├── guides/
│   ├── hooks.md
│   ├── tropes.md
│   └── taboos.md
└── embeddings/
```

### 데이터팩 인덱싱

```bash
curl -X POST http://localhost:8000/api/rag/ingest-datapack \
  -H "Content-Type: application/json" \
  -d '{"datapack_path": "data/corpus/2025Q4_romance_fantasy"}'
```

## API 문서

서버 실행 후 http://localhost:8000/docs 에서 Swagger UI를 통해 API 문서 확인 가능

주요 엔드포인트:
- `POST /api/manuscripts/upload`: 원고 업로드
- `POST /api/manuscripts/analyze`: 전체 분석 실행
- `POST /api/rag/query`: RAG 검색
- `POST /api/reports/generate`: 리포트 생성

## 개발 로드맵

### MVP (현재)
- [x] 프로젝트 구조 설계
- [ ] 기본 업로드 및 전처리
- [ ] 장르 판별 파이프라인
- [ ] RAG 서비스 구현
- [ ] 간단한 UI 및 리포트 생성

### v1.0
- [ ] 가중치 조절 UI
- [ ] 배치 분석 (여러 원고 동시 처리)
- [ ] 결과 비교 기능

### v2.0
- [ ] LangGraph 통합 (분기/병렬/체크포인트)
- [ ] 휴먼 피드백 루프
- [ ] 고급 시각화

## 기여 가이드

1. 이슈 생성 또는 기존 이슈 확인
2. 기능 브랜치 생성 (`feature/amazing-feature`)
3. 커밋 (`git commit -m 'Add amazing feature'`)
4. 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성


## 연락처

프로젝트 관리자: [유예진]
이메일: [yyj9290@naver.com]
프로젝트 링크: https://github.com/[YuYeaJin]/plotlight

## 감사의 말

- Sentence Transformers 팀
- ChromaDB 커뮤니티
- FastAPI 및 Electron 커뮤니티