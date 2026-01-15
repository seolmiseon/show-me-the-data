"""
Supabase 데이터베이스 서비스 (디버깅 버전)
"""
import os
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 일단 import만 시도
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
    logger.info("✅ Supabase 패키지 import 성공")
except ImportError as e:
    SUPABASE_AVAILABLE = False
    logger.error(f"❌ Supabase 패키지 import 실패: {e}")

from models.schemas import Event, EventType


class DatabaseService:
    """Supabase 데이터베이스 서비스"""
    
    def __init__(self):
        """Supabase 클라이언트 초기화"""
        
        # 환경변수 읽기
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        # 🔍 디버그 로그 (자세하게!)
        logger.info("=" * 50)
        logger.info("🔍 Supabase 환경변수 디버깅")
        logger.info(f"SUPABASE_URL 존재: {supabase_url is not None}")
        logger.info(f"SUPABASE_URL 값: {supabase_url}")
        logger.info(f"SUPABASE_KEY 존재: {supabase_key is not None}")
        if supabase_key:
            logger.info(f"SUPABASE_KEY 길이: {len(supabase_key)}")
            logger.info(f"SUPABASE_KEY 시작: {supabase_key[:20]}...")
            logger.info(f"SUPABASE_KEY 끝: ...{supabase_key[-20:]}")
            logger.info(f"SUPABASE_KEY 공백 포함: {' ' in supabase_key}")
        else:
            logger.info("SUPABASE_KEY: None")
        logger.info("=" * 50)
        
        # 환경변수 체크
        if not supabase_url or not supabase_key:
            error_msg = f"환경변수 누락 - URL: {supabase_url is not None}, KEY: {supabase_key is not None}"
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        # Supabase 클라이언트 생성 시도
        try:
            logger.info("🔄 Supabase 클라이언트 생성 시도...")
            self.client: Client = create_client(supabase_url, supabase_key)
            self.table_name = "events"
            logger.info("✅ Supabase 클라이언트 초기화 완료!")
        except Exception as e:
            logger.error(f"❌ Supabase 클라이언트 생성 실패: {e}")
            logger.error(f"에러 타입: {type(e).__name__}")
            logger.error(f"에러 내용: {str(e)}")
            raise
    
    async def create_event(self, event: Event) -> Event:
        """이벤트 생성"""
        try:
            event_dict = event.model_dump(exclude_none=True)
            
            if event_dict.get("datetime"):
                event_dict["datetime"] = event_dict["datetime"].isoformat()
            if event_dict.get("created_at"):
                event_dict["created_at"] = event_dict["created_at"].isoformat()
            if event_dict.get("updated_at"):
                event_dict["updated_at"] = event_dict["updated_at"].isoformat()
            
            response = self.client.table(self.table_name).insert(event_dict).execute()
            
            if not response.data:
                raise Exception("이벤트 생성 실패: 응답 데이터 없음")
            
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
        """이벤트 목록 조회"""
        try:
            query = self.client.table(self.table_name).select("*")
            
            if event_type:
                query = query.eq("event_type", event_type.value)
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            query = query.order("created_at", desc=True)
            response = query.execute()
            
            events = [Event(**item) for item in response.data]
            logger.info(f"✅ 이벤트 목록 조회: {len(events)}개")
            return events
            
        except Exception as e:
            logger.error(f"❌ 이벤트 목록 조회 오류: {e}", exc_info=True)
            raise
    
    async def get_event(self, event_id: str) -> Optional[Event]:
        """이벤트 상세 조회"""
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
        """이벤트 삭제"""
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
