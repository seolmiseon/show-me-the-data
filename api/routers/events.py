"""
Event API 라우터
이벤트 생성, 조회, 수정, 삭제 엔드포인트 (Mock Mode - 해커톤 시연용)
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
import logging
from datetime import datetime, timedelta

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

# Mock DB 서비스 (해커톤 시연용)
db = get_database_service()

# 서비스 싱글톤
_email_analyzer = None


def _get_email_analyzer():
    """EmailAnalyzer 서비스 지연 로딩"""
    global _email_analyzer
    if _email_analyzer is None:
        _email_analyzer = EmailAnalyzer()
    return _email_analyzer


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
        
        # Mock DB에 저장 (하는 척)
        event_data = {
            "summary": f"🤖 {request.text[:30]}...",
            "description": f"💡 [AI 실시간 분석]\n입력: {request.text}\n모드: {request.mode.value}",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "location": "AI 분석됨",
            "status": "confirmed",
            "created_at": datetime.now().isoformat()
        }
        
        new_event = db.create_event(event_data)
        
        # Event 스키마로 변환
        event = Event(
            id=new_event["id"],
            event_type=request.mode,
            customer_name="AI 분석 결과",
            datetime=datetime.fromisoformat(new_event["start_time"]),
            description=new_event["description"],
            original_text=request.text,
            user_id=request.user_id,
            confidence=0.95,
            extracted_fields={"ai_generated": True}
        )
        
        analysis = f"'{request.mode.value}' 이벤트가 AI 분석되어 생성되었습니다."
        
        logger.info(f"✅ 이벤트 생성 완료: {event.id}")
        
        return EventResponse(
            event=event,
            analysis=analysis,
            tokens_used=100
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
        # Mock DB에서 시나리오 데이터 조회
        mock_events = db.get_events()
        
        # Mock 데이터를 Event 스키마로 변환
        events = []
        for me in mock_events:
            event = Event(
                id=me["id"],
                event_type=EventType.WORK,  # Mock 데이터는 모두 WORK로
                customer_name=me["summary"],
                datetime=datetime.fromisoformat(me["start_time"]) if me.get("start_time") else None,
                description=me["description"],
                original_text=me["summary"],
                created_at=datetime.fromisoformat(me["created_at"]),
                confidence=0.95,
                extracted_fields={"mock": True, "location": me.get("location")}
            )
            events.append(event)
        
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
        # Mock DB에서 조회
        mock_events = db.get_events()
        mock_event = next((e for e in mock_events if e["id"] == event_id), None)
        
        if not mock_event:
            raise HTTPException(status_code=404, detail=f"이벤트를 찾을 수 없습니다: {event_id}")
        
        # Event 스키마로 변환
        event = Event(
            id=mock_event["id"],
            event_type=EventType.WORK,
            customer_name=mock_event["summary"],
            datetime=datetime.fromisoformat(mock_event["start_time"]) if mock_event.get("start_time") else None,
            description=mock_event["description"],
            original_text=mock_event["summary"],
            created_at=datetime.fromisoformat(mock_event["created_at"]),
            confidence=0.95,
            extracted_fields={}
        )
        
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
        # Mock DB에서 삭제 (하는 척)
        logger.info(f"🗑️ [Mock] 이벤트 삭제 요청: {event_id}")
        success = True  # 항상 성공
        
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
