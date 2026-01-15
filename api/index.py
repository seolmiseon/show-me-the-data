"""
FastAPI 앱 - 로컬 개발 및 Vercel 배포 공용
- 로컬 개발: python index.py 또는 uvicorn index:app 실행
- Vercel 배포: Mangum으로 자동 래핑
"""
from mangum import Mangum
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
    logger.error(f"Current sys.path: {sys.path}")
    logger.error(f"Current __file__: {__file__}")
    logger.error(f"Current dir: {os.path.dirname(os.path.abspath(__file__))}")
    events_router = None

# FastAPI 앱 초기화
app = FastAPI(
    title="Show Me The Data",
    version="1.0.0",
    description="AI Business Dashboard - 이메일/메시지 분석 및 일정 관리",
    docs_url="/docs",
    redoc_url="/redoc",
)

logger.info("🏗️ FastAPI 앱 초기화 완료")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 구체적인 도메인으로 제한 권장
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


@app.get("/", tags=["Root"])
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Show Me The Data API is running!",
        "version": "1.0.0",
        "timestamp": str(datetime.now()),
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """헬스 체크 엔드포인트"""
    openai_configured = (
        "configured" if os.getenv("OPENAI_API_KEY") else "not configured"
    )

    return {
        "status": "healthy",
        "service": "Show Me The Data API",
        "openai": openai_configured,
        "timestamp": str(datetime.now()),
    }


# 로컬 개발용: 직접 실행 가능
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8082))
    logger.info(f"🚀 로컬 서버 시작: http://localhost:{port}")
    uvicorn.run("index:app", host="0.0.0.0", port=port, reload=True)

# Vercel 배포용: Mangum으로 래핑
# Vercel이 자동으로 이 handler를 사용
handler = Mangum(app, lifespan="off")
