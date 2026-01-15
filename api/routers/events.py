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

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"])

# 임시 저장소 (실제로는 DB 사용)
events_store: List[Event] = []

# EmailAnalyzer 초기화
email_analyzer = EmailAnalyzer()


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
        
        # 이메일/메시지 분석
        event = await email_analyzer.analyze(
            text=request.text,
            mode=request.mode,
            user_id=request.user_id
        )
        
        # ID 생성 (실제로는 DB에서 생성)
        event.id = f"event_{len(events_store) + 1}_{datetime.now().timestamp()}"
        
        # 저장 (실제로는 DB에 저장)
        events_store.append(event)
        
        # 분석 결과 설명 생성
        analysis = f"'{event.customer_name or '이름 없음'}'의 {request.mode.value} 이벤트가 생성되었습니다."
        if event.datetime:
            analysis += f" 일정: {event.datetime.strftime('%Y-%m-%d %H:%M')}"
        
        # 토큰 수 계산 (대략적)
        tokens_used = email_analyzer.openai_service.count_tokens(request.text)
        
        logger.info(f"✅ 이벤트 생성 완료: {event.id}")
        
        return EventResponse(
            event=event,
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
        # 필터링
        filtered_events = events_store.copy()
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.event_type == event_type]
        
        if user_id:
            filtered_events = [e for e in filtered_events if e.user_id == user_id]
        
        # 최신순 정렬
        filtered_events.sort(key=lambda x: x.created_at, reverse=True)
        
        logger.info(f"✅ 이벤트 목록 조회: {len(filtered_events)}개")
        
        return EventListResponse(
            events=filtered_events,
            total=len(filtered_events)
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
        # 이벤트 찾기
        event = next((e for e in events_store if e.id == event_id), None)
        
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
        global events_store
        
        # 이벤트 찾기
        event_index = next(
            (i for i, e in enumerate(events_store) if e.id == event_id),
            None
        )
        
        if event_index is None:
            raise HTTPException(
                status_code=404,
                detail=f"이벤트를 찾을 수 없습니다: {event_id}"
            )
        
        # 삭제
        deleted_event = events_store.pop(event_index)
        
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
