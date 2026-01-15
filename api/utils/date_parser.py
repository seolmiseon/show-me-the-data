"""
날짜 파싱 유틸리티
FSF 프로젝트의 calendar_tool.py에서 parse_date 함수 복사
"""
from typing import Optional
from datetime import datetime, timedelta
import re
import logging

logger = logging.getLogger(__name__)


def parse_date(date_str: str) -> Optional[str]:
    """
    날짜 문자열을 파싱하여 YYYY-MM-DD 형식으로 반환
    
    Args:
        date_str: 날짜 문자열 (예: "오늘", "내일", "2025-12-25", "12월 25일")
    
    Returns:
        YYYY-MM-DD 형식의 날짜 문자열 또는 None
    """
    try:
        date_str = date_str.strip().lower()
        today = datetime.now()
        
        # "오늘" 처리
        if date_str in ["오늘", "today"]:
            return today.strftime("%Y-%m-%d")
        
        # "내일" 처리
        if date_str in ["내일", "tomorrow"]:
            tomorrow = today + timedelta(days=1)
            return tomorrow.strftime("%Y-%m-%d")
        
        # "어제" 처리
        if date_str in ["어제", "yesterday"]:
            yesterday = today - timedelta(days=1)
            return yesterday.strftime("%Y-%m-%d")
        
        # 이미 YYYY-MM-DD 형식인 경우
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
        
        # "12월 25일" 형식 처리
        month_day_match = re.search(r'(\d{1,2})월\s*(\d{1,2})일', date_str)
        if month_day_match:
            month = int(month_day_match.group(1))
            day = int(month_day_match.group(2))
            # 올해로 가정 (다음 해인 경우는 고려하지 않음)
            year = today.year
            try:
                parsed_date = datetime(year, month, day)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                return None
        
        # "12/25" 형식 처리
        slash_match = re.search(r'(\d{1,2})/(\d{1,2})', date_str)
        if slash_match:
            month = int(slash_match.group(1))
            day = int(slash_match.group(2))
            year = today.year
            try:
                parsed_date = datetime(year, month, day)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                return None
        
        return None
        
    except Exception as e:
        logger.error(f"❌ 날짜 파싱 오류: {e}")
        return None
