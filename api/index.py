# from mangum import Mangum  <-- ❌ 삭제! (이게 원흉입니다)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import logging
from datetime import datetime

# Vercel 배포를 위한 경로 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 라우터 import
try:
    from routers.events import router as events_router
    logger.info("✅ Events 라우터 import 성공")
except Exception as e:
    logger.error(f"❌ Events 라우터 import 실패: {e}")
    # 경로 디버깅용 로그
    logger.error(f"Current sys.path: {sys.path}")
    events_router = None

# FastAPI 앱 초기화 (전역 변수 'app' 필수)
app = FastAPI(
    title="Show Me The Data",
    version="1.0.0",
    description="AI Business Dashboard",
    docs_url="/docs",
    redoc_url="/redoc",
)

logger.info("🏗️ FastAPI 앱 초기화 완료")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

logger.info("🔐 CORS 미들웨어 등록 완료")

# 라우터 등록
if events_router:
    app.include_router(events_router, prefix="/api")
    logger.info("✅ Events 라우터 등록 완료")

logger.info("🔗 모든 라우터 등록 완료!")

@app.get("/api/health") # Vercel 경로 매칭을 위해 /api prefix 붙임
async def health_check():
    return {
        "status": "healthy",
        "timestamp": str(datetime.now()),
    }

# 로컬 개발용
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8082))
    logger.info(f"🚀 로컬 서버 시작: http://localhost:{port}")
    uvicorn.run("index:app", host="0.0.0.0", port=port, reload=True)

# ❌ 삭제: handler = Mangum(app) 
# Vercel은 'app' 변수를 자동으로 찾아서 실행합니다.