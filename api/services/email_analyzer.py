"""
이메일/메시지 분석 서비스 (Agent 시스템 사용)
FSF 프로젝트의 Agent 구조를 재사용하여 정보 추출
"""
from typing import Dict, Optional
from datetime import datetime
import json
import logging

from models.schemas import EventType, Event
from services.openai_service import OpenAIService
from utils.date_parser import parse_date
from agents.event_agent import EventAgent

logger = logging.getLogger(__name__)


class EmailAnalyzer:
    """이메일/메시지 분석 서비스 (Agent 시스템 사용)"""
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.event_agent = EventAgent()
    
    def _get_system_prompt(self, mode: EventType) -> str:
        """
        모드에 따른 System Prompt 반환 (Prompt Switching)
        
        Args:
            mode: 이벤트 타입 (recruit/order/work)
        
        Returns:
            System Prompt 문자열
        """
        prompts = {
            EventType.RECRUIT: """당신은 채용 담당자를 위한 AI 어시스턴트입니다.
이메일이나 메시지에서 다음 정보를 추출해주세요:
1. 지원자 이름
2. 면접 날짜와 시간
3. 면접 관련 설명

JSON 형식으로 반환해주세요:
{
    "customer_name": "지원자 이름",
    "datetime": "YYYY-MM-DD HH:MM 형식 (없으면 null)",
    "description": "면접 관련 설명"
}""",
            
            EventType.ORDER: """당신은 예약/주문 관리자를 위한 AI 어시스턴트입니다.
이메일이나 메시지에서 다음 정보를 추출해주세요:
1. 고객 이름
2. 예약/픽업 날짜와 시간
3. 예약 관련 설명

JSON 형식으로 반환해주세요:
{
    "customer_name": "고객 이름",
    "datetime": "YYYY-MM-DD HH:MM 형식 (없으면 null)",
    "description": "예약 관련 설명"
}""",
            
            EventType.WORK: """당신은 프리랜서/1인 대행사를 위한 AI 어시스턴트입니다.
이메일이나 메시지에서 다음 정보를 추출해주세요:
1. 클라이언트 이름
2. 미팅/작업 마감일 날짜와 시간
3. 작업 요청 내용 설명

JSON 형식으로 반환해주세요:
{
    "customer_name": "클라이언트 이름",
    "datetime": "YYYY-MM-DD HH:MM 형식 (없으면 null)",
    "description": "작업 요청 내용"
}"""
        }
        return prompts.get(mode, prompts[EventType.WORK])
    
    async def analyze(self, text: str, mode: EventType, user_id: Optional[str] = None) -> Event:
        """
        이메일/메시지 분석 및 Event 생성 (Agent 시스템 사용)
        
        Args:
            text: 분석할 텍스트 (이메일/메시지 본문)
            mode: 이벤트 타입 (recruit/order/work)
            user_id: 사용자 ID (선택적)
        
        Returns:
            Event 객체
        """
        try:
            # Agent를 사용하여 분석 (FSF 구조 재사용)
            response_text = await self.event_agent.analyze(
                text=text,
                mode=mode,
                user_id=user_id
            )
            
            # JSON 파싱 시도
            extracted_data = self._parse_json_response(response_text)
            
            # 날짜/시간 파싱
            datetime_obj = None
            if extracted_data.get("datetime"):
                datetime_obj = self._parse_datetime(extracted_data["datetime"], text)
            
            # Event 객체 생성
            event = Event(
                event_type=mode,
                customer_name=extracted_data.get("customer_name"),
                datetime=datetime_obj,
                description=extracted_data.get("description"),
                original_text=text,
                user_id=user_id,
                confidence=0.8,  # 기본 신뢰도
                extracted_fields=extracted_data
            )
            
            logger.info(f"✅ 이메일 분석 완료: {mode.value} - {event.customer_name}")
            return event
            
        except Exception as e:
            logger.error(f"❌ 이메일 분석 오류: {e}", exc_info=True)
            # 오류 발생 시 기본 Event 반환
            return Event(
                event_type=mode,
                customer_name=None,
                datetime=None,
                description="분석 중 오류가 발생했습니다.",
                original_text=text,
                user_id=user_id,
                confidence=0.0,
                extracted_fields={"error": str(e)}
            )
    
    def _parse_json_response(self, response_text: str) -> Dict:
        """
        LLM 응답에서 JSON 추출
        
        Args:
            response_text: LLM 응답 텍스트
        
        Returns:
            파싱된 JSON 딕셔너리
        """
        try:
            # JSON 코드 블록 제거
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            # JSON 파싱
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트에서 정보 추출 시도
            logger.warning("JSON 파싱 실패, 텍스트에서 정보 추출 시도")
            return {
                "customer_name": None,
                "datetime": None,
                "description": response_text
            }
    
    def _parse_datetime(self, datetime_str: str, original_text: str) -> Optional[datetime]:
        """
        날짜/시간 문자열을 datetime 객체로 변환
        
        Args:
            datetime_str: 날짜/시간 문자열 (예: "2025-01-15 14:00" 또는 "목요일 3시")
            original_text: 원본 텍스트 (추가 파싱 시 사용)
        
        Returns:
            datetime 객체 또는 None
        """
        try:
            # 이미 "YYYY-MM-DD HH:MM" 형식인 경우
            if " " in datetime_str and len(datetime_str) > 10:
                try:
                    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    pass
            
            # 날짜만 있는 경우 (date_parser 사용)
            date_str = parse_date(datetime_str)
            if date_str:
                # 시간은 원본 텍스트에서 추출 시도
                time_match = self._extract_time(original_text)
                if time_match:
                    hour, minute = time_match
                    return datetime.strptime(f"{date_str} {hour:02d}:{minute:02d}", "%Y-%m-%d %H:%M")
                else:
                    # 시간 없으면 날짜만 반환
                    return datetime.strptime(date_str, "%Y-%m-%d")
            
            return None
        except Exception as e:
            logger.error(f"날짜/시간 파싱 오류: {e}")
            return None
    
    def _extract_time(self, text: str) -> Optional[tuple]:
        """
        텍스트에서 시간 추출 (HH, MM)
        
        Args:
            text: 원본 텍스트
        
        Returns:
            (hour, minute) 튜플 또는 None
        """
        import re
        
        # "3시", "14시", "오후 3시" 등 패턴
        time_patterns = [
            r'(\d{1,2})시',
            r'오후\s*(\d{1,2})시',
            r'오전\s*(\d{1,2})시',
            r'(\d{1,2}):(\d{1,2})',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                if len(match.groups()) == 2:  # "14:30" 형식
                    hour = int(match.group(1))
                    minute = int(match.group(2))
                    return (hour, minute)
                else:  # "3시" 형식
                    hour = int(match.group(1))
                    # "오후" 키워드 확인
                    if "오후" in text and hour < 12:
                        hour += 12
                    return (hour, 0)
        
        return None
