"""
이벤트 정보 추출 Tool
FSF 프로젝트의 calendar_tool.py 구조를 참고하여 생성
"""
from langchain.tools import Tool
from typing import Optional
import logging
import json
from datetime import datetime

from models.schemas import EventType
from utils.date_parser import parse_date

logger = logging.getLogger(__name__)


def extract_event_info(text: str, mode: str = "work") -> str:
    """
    텍스트에서 이벤트 정보를 추출합니다.
    
    Args:
        text: 분석할 텍스트 (이메일/메시지 본문)
        mode: 이벤트 타입 ("recruit", "order", "work")
    
    Returns:
        JSON 형식의 추출된 정보 문자열
    """
    try:
        # 이 함수는 LLM이 이미 추출한 정보를 파싱하거나,
        # 간단한 패턴 매칭으로 정보를 추출합니다.
        # 실제 추출은 Agent의 LLM이 수행하고, 여기서는 결과를 정리합니다.
        
        # JSON 형식인 경우 파싱
        if text.strip().startswith("{") or "customer_name" in text.lower():
            try:
                json_text = text
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0]
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0]
                
                extracted = json.loads(json_text.strip())
                return json.dumps(extracted, ensure_ascii=False)
            except json.JSONDecodeError:
                pass
        
        # 텍스트 그대로 반환 (LLM이 처리하도록)
        return text
        
    except Exception as e:
        logger.error(f"❌ 이벤트 정보 추출 오류: {e}", exc_info=True)
        return json.dumps({
            "customer_name": None,
            "datetime": None,
            "description": f"추출 중 오류 발생: {str(e)}"
        }, ensure_ascii=False)


# LangChain Tool로 변환 (FSF의 CalendarTool 구조 참고)
EventExtractionTool = Tool(
    name="extract_event_info",
    description="이메일이나 메시지에서 이벤트 정보(고객 이름, 날짜/시간, 설명)를 추출하는 도구입니다. 텍스트를 분석하여 JSON 형식으로 정보를 반환합니다.",
    func=lambda text: extract_event_info(text.strip())
)
