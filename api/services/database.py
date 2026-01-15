"""
Supabase 데이터베이스 서비스
"""
import os
from typing import List, Optional
from datetime import datetime
from supabase import create_client, Client
import logging

from models.schemas import Event, EventType

logger = logging.getLogger(__name__)


class DatabaseService:
    """Supabase 데이터베이스 서비스"""
    
    def __init__(self):
        """Supabase 클라이언트 초기화"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL과 SUPABASE_KEY 환경 변수가 필요합니다.")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        self.table_name = "events"
        logger.info("✅ Supabase 클라이언트 초기화 완료")
    
    async def create_event(self, event: Event) -> Event:
        """
        이벤트 생성
        
        Args:
            event: Event 객체
        
        Returns:
            Event: 생성된 이벤트 (ID 포함)
        """
        try:
            # Event를 dict로 변환
            event_dict = event.model_dump(exclude_none=True)
            
            # datetime을 ISO 문자열로 변환
            if event_dict.get("datetime"):
                event_dict["datetime"] = event_dict["datetime"].isoformat()
            if event_dict.get("created_at"):
                event_dict["created_at"] = event_dict["created_at"].isoformat()
            if event_dict.get("updated_at"):
                event_dict["updated_at"] = event_dict["updated_at"].isoformat()
            
            # Supabase에 삽입
            response = self.client.table(self.table_name).insert(event_dict).execute()
            
            if not response.data:
                raise Exception("이벤트 생성 실패: 응답 데이터 없음")
            
            # 생성된 이벤트 반환
            created_event = Event(**response.data[0])
            logger.info(f"✅ 이벤트 생성 완료: {created_event.id}")
            return created_event
            
        except Exception as e:
            logger.error(f"❌ 이벤트 생성 오류: {e}", exc_info=True)
            raise
    
    async def get_events(
        self,
        event_type: Optional[EventType] = None,
        user_id: Optional[str] = None
    ) -> List[Event]:
        """
        이벤트 목록 조회
        
        Args:
            event_type: 이벤트 타입 필터
            user_id: 사용자 ID 필터
        
        Returns:
            List[Event]: 이벤트 목록
        """
        try:
            # 쿼리 생성
            query = self.client.table(self.table_name).select("*")
            
            # 필터 적용
            if event_type:
                query = query.eq("event_type", event_type.value)
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            # 최신순 정렬
            query = query.order("created_at", desc=True)
            
            # 실행
            response = query.execute()
            
            # Event 객체로 변환
            events = [Event(**item) for item in response.data]
            
            logger.info(f"✅ 이벤트 목록 조회: {len(events)}개")
            return events
            
        except Exception as e:
            logger.error(f"❌ 이벤트 목록 조회 오류: {e}", exc_info=True)
            raise
    
    async def get_event(self, event_id: str) -> Optional[Event]:
        """
        이벤트 상세 조회
        
        Args:
            event_id: 이벤트 ID
        
        Returns:
            Optional[Event]: 이벤트 또는 None
        """
        try:
            response = (
                self.client.table(self.table_name)
                .select("*")
                .eq("id", event_id)
                .execute()
            )
            
            if not response.data:
                return None
            
            event = Event(**response.data[0])
            logger.info(f"✅ 이벤트 상세 조회: {event_id}")
            return event
            
        except Exception as e:
            logger.error(f"❌ 이벤트 상세 조회 오류: {e}", exc_info=True)
            raise
    
    async def delete_event(self, event_id: str) -> bool:
        """
        이벤트 삭제
        
        Args:
            event_id: 이벤트 ID
        
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            response = (
                self.client.table(self.table_name)
                .delete()
                .eq("id", event_id)
                .execute()
            )
            
            if not response.data:
                return False
            
            logger.info(f"✅ 이벤트 삭제 완료: {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 이벤트 삭제 오류: {e}", exc_info=True)
            raise


# 싱글톤 인스턴스
_db_service: Optional[DatabaseService] = None


def get_database_service() -> DatabaseService:
    """데이터베이스 서비스 싱글톤 반환"""
    global _db_service
    
    if _db_service is None:
        _db_service = DatabaseService()
    
    return _db_service
