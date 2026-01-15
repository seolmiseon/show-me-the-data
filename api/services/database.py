"""
Mock 데이터베이스 서비스 (해커톤용 임시)
실제 DB 연동은 다음 버전에서!
"""
import logging
from datetime import datetime
import uuid
from typing import List, Optional
from models.schemas import Event, EventType

logger = logging.getLogger(__name__)


class MockDatabaseService:
    """Mock DB 서비스 (Supabase 대신 사용)"""
    
    def __init__(self):
        logger.info("🎭 Mock DB 서비스가 실행됩니다. (메모리 저장)")
        
        # 메모리 저장소 (새로고침하면 사라짐!)
        self.events_memory = []
        
        # 시연용 더미 데이터 (처음 시작시에만 추가)
        self.dummy_events = [
            Event(
                id="mock-1",
                event_type=EventType.WORK,
                customer_name="패스트캠퍼스",
                datetime=datetime.now(),
                description="해커톤 마감일! 무조건 제출한다.",
                original_text="[해커톤] 쇼미더데이터 프로젝트 제출",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                confidence=1.0,
                extracted_fields={}
            ),
            Event(
                id="mock-2",
                event_type=EventType.WORK,
                customer_name="팀원들",
                datetime=datetime(2026, 1, 23, 19, 0),
                description="해커톤 끝나고 고기 먹으러 감",
                original_text="팀 회식 - 강남역 19시",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                confidence=0.9,
                extracted_fields={}
            )
        ]
        
        # 더미 데이터를 메모리에 추가
        self.events_memory.extend(self.dummy_events)
    
    async def create_event(self, event: Event) -> Event:
        """이벤트 생성 및 메모리에 저장"""
        logger.info(f"📝 [Mock] 이벤트 생성 요청 받음: {event.customer_name}")
        
        # ID 생성
        event.id = str(uuid.uuid4())
        event.created_at = datetime.now()
        event.updated_at = datetime.now()
        
        # 메모리에 저장!
        self.events_memory.append(event)
        
        logger.info(f"✅ [Mock] 이벤트 생성 완료: {event.id}")
        logger.info(f"📊 현재 저장된 이벤트 수: {len(self.events_memory)}")
        return event
    
    async def get_events(
        self,
        event_type: Optional[EventType] = None,
        user_id: Optional[str] = None
    ) -> List[Event]:
        """이벤트 목록 조회 (메모리에서)"""
        logger.info("📂 [Mock] 이벤트 목록 조회 요청")
        
        # 메모리에서 가져오기
        events = self.events_memory
        
        # 필터링 (옵션)
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        # 최신순 정렬
        events = sorted(events, key=lambda x: x.created_at, reverse=True)
        
        logger.info(f"✅ [Mock] {len(events)}개 이벤트 리턴")
        return events
    
    async def get_event(self, event_id: str) -> Optional[Event]:
        """이벤트 상세 조회"""
        logger.info(f"🔍 [Mock] 이벤트 상세 조회: {event_id}")
        
        for event in self.events_memory:
            if event.id == event_id:
                return event
        return None
    
    async def delete_event(self, event_id: str) -> bool:
        """이벤트 삭제하는 척"""
        logger.info(f"🗑️ [Mock] 이벤트 삭제 요청: {event_id}")
        # 실제로는 삭제 안 하지만 성공 리턴
        return True


# 싱글톤 인스턴스
_db_service: Optional[MockDatabaseService] = None


def get_database_service() -> MockDatabaseService:
    """데이터베이스 서비스 싱글톤 반환"""
    global _db_service
    
    if _db_service is None:
        _db_service = MockDatabaseService()
    
    return _db_service
