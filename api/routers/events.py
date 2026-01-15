"""
Event API 라우터
이벤트 생성, 조회, 수정, 삭제 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
import logging
from datetime import datetime

from models.schemas import (
    EventRequest,
    EventResponse,
    EventListResponse,
    Event,
    EventType
)
from services.email_analyzer import EmailAnalyzer
from services.database import get_database_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"])

# 서비스 싱글톤
_email_analyzer = None
_db_service = None


def _get_email_analyzer():
    """EmailAnalyzer 서비스 지연 로딩"""
    global _email_analyzer
    if _email_analyzer is None:
        _email_analyzer = EmailAnalyzer()
    return _email_analyzer


def _get_db():
    """데이터베이스 서비스 지연 로딩"""
    global _db_service
    if _db_service is None:
        _db_service = get_database_service()
    return _db_service


@router.post(
    "",
    response_model=EventResponse,
    summary="이벤트 생성 (이메일/메시지 분석)",
    description="이메일이나 메시지를 분석하여 Event를 생성합니다."
)
async def create_event(request: EventRequest) -> EventResponse:
    """
    이벤트 생성 엔드포인트
    
    Args:
        request: EventRequest (text, mode, user_id)
    
    Returns:
        EventResponse: 생성된 이벤트와 분석 결과
    """
    try:
        logger.info(f"📧 이벤트 생성 요청: {request.mode.value} - {request.text[:50]}...")
        
        # 서비스 가져오기
        analyzer = _get_email_analyzer()
        db = _get_db()
        
        # 이메일/메시지 분석
        event = await analyzer.analyze(
            text=request.text,
            mode=request.mode,
            user_id=request.user_id
        )
        
        # 데이터베이스에 저장
        saved_event = await db.create_event(event)
        
        # 분석 결과 설명 생성
        analysis = f"'{saved_event.customer_name or '이름 없음'}'의 {request.mode.value} 이벤트가 생성되었습니다."
        if saved_event.datetime:
            analysis += f" 일정: {saved_event.datetime.strftime('%Y-%m-%d %H:%M')}"
        
        # 토큰 수 계산 (대략적)
        tokens_used = analyzer.openai_service.count_tokens(request.text)
        
        logger.info(f"✅ 이벤트 생성 완료: {saved_event.id}")
        
        return EventResponse(
            event=saved_event,
            analysis=analysis,
            tokens_used=tokens_used
        )
        
    except Exception as e:
        logger.error(f"❌ 이벤트 생성 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"이벤트 생성 실패: {str(e)}"
        )


@router.get(
    "",
    response_model=EventListResponse,
    summary="이벤트 목록 조회",
    description="모든 이벤트 목록을 조회합니다."
)
async def get_events(
    event_type: Optional[EventType] = None,
    user_id: Optional[str] = None
) -> EventListResponse:
    """
    이벤트 목록 조회 엔드포인트
    
    Args:
        event_type: 이벤트 타입 필터 (선택적)
        user_id: 사용자 ID 필터 (선택적)
    
    Returns:
        EventListResponse: 이벤트 목록
    """
    try:
        # 데이터베이스에서 조회
        db = _get_db()
        events = await db.get_events(event_type=event_type, user_id=user_id)
        
        logger.info(f"✅ 이벤트 목록 조회: {len(events)}개")
        
        return EventListResponse(
            events=events,
            total=len(events)
        )
        
    except Exception as e:
        logger.error(f"❌ 이벤트 목록 조회 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"이벤트 목록 조회 실패: {str(e)}"
        )


@router.get(
    "/{event_id}",
    response_model=Event,
    summary="이벤트 상세 조회",
    description="특정 이벤트의 상세 정보를 조회합니다."
)
async def get_event(event_id: str) -> Event:
    """
    이벤트 상세 조회 엔드포인트
    
    Args:
        event_id: 이벤트 ID
    
    Returns:
        Event: 이벤트 상세 정보
    """
    try:
        # 데이터베이스에서 조회
        db = _get_db()
        event = await db.get_event(event_id)
        
        if not event:
            raise HTTPException(
                status_code=404,
                detail=f"이벤트를 찾을 수 없습니다: {event_id}"
            )
        
        logger.info(f"✅ 이벤트 상세 조회: {event_id}")
        return event
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 이벤트 상세 조회 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"이벤트 상세 조회 실패: {str(e)}"
        )


@router.delete(
    "/{event_id}",
    summary="이벤트 삭제",
    description="특정 이벤트를 삭제합니다."
)
async def delete_event(event_id: str) -> dict:
    """
    이벤트 삭제 엔드포인트
    
    Args:
        event_id: 이벤트 ID
    
    Returns:
        삭제 결과
    """
    try:
        # 데이터베이스에서 삭제
        db = _get_db()
        success = await db.delete_event(event_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"이벤트를 찾을 수 없습니다: {event_id}"
            )
        
        logger.info(f"✅ 이벤트 삭제 완료: {event_id}")
        
        return {
            "message": "이벤트가 삭제되었습니다.",
            "event_id": event_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 이벤트 삭제 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"이벤트 삭제 실패: {str(e)}"
        )
