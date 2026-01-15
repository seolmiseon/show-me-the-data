# Show Me The Data

> AI Business Dashboard - 이메일/메시지 분석 및 일정 관리

**Live Demo**: [https://show-me-the-data.vercel.app](https://show-me-the-data.vercel.app)

---

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone <repository-url>
cd show-me-the-data
```

### 2. 프론트엔드 설정

```bash
# 패키지 설치
npm install

# 환경 변수 설정 (선택사항)
cp .env.example .env
# .env 파일에서 NEXT_PUBLIC_API_URL 수정

# 개발 서버 실행
npm run dev
```

프론트엔드: http://localhost:3000

### 3. 백엔드 로컬 개발

```bash
cd api

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r ../requirements.txt

# 환경 변수 설정 (.env 파일)
echo "OPENAI_API_KEY=your-api-key" > .env

# 서버 실행
python index.py
# 또는
uvicorn index:app --reload --port 8082
```

백엔드 API: http://localhost:8082  
API 문서: http://localhost:8082/docs

### 4. Vercel 배포

**환경 변수 설정** (Vercel 대시보드):
- `OPENAI_API_KEY`: OpenAI API 키

**배포**:
```bash
git push origin main
```

자동 배포 완료! 🚀

---

## 📋 주요 기능

### 1. 이메일/메시지 분석
- 텍스트에서 날짜/시간 자동 추출
- 고객/클라이언트 이름 추출
- 모드별 맞춤 분석 (채용/예약/업무)

### 2. 일정 관리
- FullCalendar 기반 캘린더 뷰
- 이벤트 자동 등록
- 이벤트 조회/삭제

### 3. 모드 전환
- **채용 모드**: 지원자 면접 일정 관리
- **예약 모드**: 고객 예약 관리
- **업무 모드**: 클라이언트 미팅/작업 요청 관리

---

## 🏗 프로젝트 구조

```
show-me-the-data/
├── app/                      # Next.js 프론트엔드
│   ├── dashboard/
│   │   └── page.tsx          # 대시보드 UI
│   ├── page.tsx              # 메인 페이지
│   └── layout.tsx            # 레이아웃
│
├── api/                      # FastAPI 백엔드 (로컬/Vercel 공용)
│   ├── index.py              # 진입점 (로컬: uvicorn, Vercel: Mangum)
│   ├── models/
│   │   └── schemas.py        # Event 통합 모델
│   ├── services/
│   │   ├── email_analyzer.py # 이메일 분석 (ExtractionChain)
│   │   └── openai_service.py # OpenAI 서비스
│   ├── routers/
│   │   └── events.py         # Event API 라우터
│   └── utils/
│       └── date_parser.py    # 날짜 파싱
│
├── vercel.json               # Vercel 설정 (API 라우팅)
├── requirements.txt          # Python 패키지
└── package.json              # Node.js 패키지
```

---

## 🔧 기술 스택

### Frontend
- **Framework**: Next.js 16.1
- **UI**: Tailwind CSS
- **Calendar**: FullCalendar
- **Language**: TypeScript

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **LLM**: OpenAI GPT-4o-mini
- **Validation**: Pydantic 2.x

---

## 📡 API 엔드포인트

### 이벤트 생성
```bash
POST /api/events
Content-Type: application/json

{
  "text": "김철수 클라이언트: 이번 주 목요일 3시에 미팅합시다.",
  "mode": "work",
  "user_id": null
}
```

### 이벤트 목록 조회
```bash
GET /api/events?event_type=work&user_id=user123
```

### 이벤트 상세 조회
```bash
GET /api/events/{event_id}
```

### 이벤트 삭제
```bash
DELETE /api/events/{event_id}
```

---

## 🌐 배포

### Vercel (Full Stack)
- 배포 주소: https://show-me-the-data.vercel.app
- 자동 배포: Git push 시 자동 배포
- **프론트엔드 + 백엔드 모두 Vercel Serverless Functions로 배포**
- 별도 서버 불필요: 모든 것이 Vercel에서 실행됨

### 배포 구조
- **프론트엔드**: Next.js (Vercel 자동 배포)
- **백엔드**: FastAPI → Mangum → Vercel Python Runtime
- **API 경로**: `/api/*` → `api/index.py` (vercel.json 설정)

---

## 📝 환경 변수

### Frontend (.env)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8082/api
```

### Backend (server/.env)
```bash
OPENAI_API_KEY=your-openai-api-key
PORT=8082
```

---

## 🧪 테스트

### 백엔드 테스트
```bash
cd server
source venv/bin/activate
python test_api.py
```

### API 테스트
- Swagger UI: http://localhost:8082/docs
- Health Check: http://localhost:8082/health

---

## 📄 라이선스

MIT License

---

## 👤 작성자

**seolmiseon**
- GitHub: [@seolmiseon](https://github.com/seolmiseon)

---

<div align="center">

**Made with ❤️ by seolmiseon**

[![Live Demo](https://img.shields.io/badge/Live_Demo-show--me--the--data.vercel.app-000000?style=for-the-badge&logo=vercel)](https://show-me-the-data.vercel.app)

</div>
