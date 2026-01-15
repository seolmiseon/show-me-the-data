# API - 로컬 개발 및 Vercel 배포 공용

## 🚀 로컬 개발

### 1. 가상환경 생성 및 패키지 설치

```bash
cd api

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치 (루트의 requirements.txt 사용)
pip install -r ../requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일 생성 (프로젝트 루트 또는 api/ 폴더):

```bash
OPENAI_API_KEY=your-openai-api-key
PORT=8082
```

### 3. 서버 실행

```bash
# 방법 1: Python으로 직접 실행
python index.py

# 방법 2: uvicorn으로 실행
uvicorn index:app --reload --port 8082
```

서버 실행 후:
- API: http://localhost:8082
- API 문서: http://localhost:8082/docs
- Health Check: http://localhost:8082/health

---

## 🌐 Vercel 배포

### 자동 배포

Git push만 하면 자동 배포:

```bash
git add .
git commit -m "Update API"
git push origin main
```

Vercel이 자동으로:
1. `requirements.txt` 읽어서 패키지 설치
2. `api/index.py`를 Serverless Function으로 변환
3. `handler = Mangum(app)` 사용하여 배포

### 환경 변수 설정

Vercel 대시보드 → Settings → Environment Variables:
- `OPENAI_API_KEY`: OpenAI API 키

---

## 📁 구조

```
api/
├── index.py              # FastAPI 앱 (로컬/Vercel 공용)
├── models/               # Pydantic 모델
├── services/             # 비즈니스 로직
├── routers/              # FastAPI 라우터
└── utils/                # 유틸리티 함수
```

**중요**: 
- 로컬 개발: `python index.py` 또는 `uvicorn index:app`
- Vercel 배포: 자동으로 `handler` 사용
- **하나의 코드베이스로 로컬과 배포 모두 처리**
