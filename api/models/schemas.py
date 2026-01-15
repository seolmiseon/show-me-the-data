from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime as dt
from enum import Enum


class EventType(str, Enum):
    """이벤트 타입"""
    RECRUIT = "recruit"  # 채용 (면접 일정)
    ORDER = "order"      # 주문/예약 (고객 예약)
    WORK = "work"        # 업무 (클라이언트 미팅, 작업 요청)


class EventRequest(BaseModel):
    """이벤트 생성 요청 (이메일/메시지 분석용)"""
    text: str = Field(..., description="이메일 또는 메시지 본문", example="김철수 클라이언트: 이번 주 목요일 3시에 미팅합시다.")
    mode: EventType = Field(..., description="분석 모드 (recruit/order/work)")
    user_id: Optional[str] = Field(default=None, description="사용자 ID")


class Event(BaseModel):
    """통합 이벤트 모델 (One Table Strategy)"""
    id: Optional[str] = None
    event_type: EventType
    customer_name: Optional[str] = None
    datetime: Optional[dt] = None
    description: Optional[str] = None
    original_text: str
    
    # 메타데이터
    created_at: dt = Field(default_factory=dt.now)
    updated_at: dt = Field(default_factory=dt.now)
    user_id: Optional[str] = None
    
    # AI 분석 결과
    confidence: float = Field(default=0.0, ge=0, le=1)
    extracted_fields: dict = Field(default_factory=dict)


class EventResponse(BaseModel):
    """이벤트 생성 응답"""
    event: Event = Field(..., description="생성된 이벤트")
    analysis: str = Field(..., description="AI 분석 결과 설명")
    tokens_used: int = Field(default=0, description="사용된 토큰 수")


class EventListResponse(BaseModel):
    """이벤트 목록 응답"""
    events: List[Event] = Field(default=[], description="이벤트 목록")
    total: int = Field(default=0, description="전체 개수")
