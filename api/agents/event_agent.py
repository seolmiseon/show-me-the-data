"""
Event Agent
FSF 프로젝트의 agent.py 구조를 재사용하여 이메일/메시지 분석에 적용
"""
from fastapi import HTTPException
from typing import Optional
import logging
import os
import asyncio
from datetime import datetime

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

from services.openai_service import OpenAIService
from tools import EventExtractionTool
from models.schemas import EventType

logger = logging.getLogger(__name__)

# 전역 변수 (Lazy Loading용)
_openai_service = None
_llm = None
_base_agent = None


def _get_openai_service():
    """OpenAI 서비스 지연 로딩"""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service


def _get_llm():
    """LangChain LLM 지연 로딩"""
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
            temperature=0.7
        )
    return _llm


def _get_base_agent():
    """Agent 지연 로딩"""
    global _base_agent
    if _base_agent is None:
        base_tools = [EventExtractionTool]
        _base_agent = initialize_agent(
            tools=base_tools,
            llm=_get_llm(),
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
    return _base_agent

# Agent 시스템 프롬프트 (FSF의 ReAct 프롬프트 구조 참고)
REACT_AGENT_SYSTEM_PROMPT = """당신은 이메일/메시지 분석 전문 AI 어시스턴트입니다.

**중요: 반드시 다음 형식을 지켜야 합니다:**

[생각] 현재 상황을 분석하고, 필요한 정보를 파악합니다.
[행동] 적절한 도구를 선택하고 실행합니다.
[결과] 도구 실행 결과를 확인하고, 다음 단계를 결정합니다.

**도구 사용 원칙:**
1. 이메일이나 메시지에서 고객 이름, 날짜/시간, 설명을 정확히 추출하세요.
2. 도구 실행이 실패하면, 다른 방법을 시도하거나 에러를 명확히 보고하세요.
3. 사용자의 요청에 정확하게 답변하기 위해 필요한 모든 도구를 사용하세요.

**추출 형식:**
JSON 형식으로 다음 정보를 추출하세요:
{
    "customer_name": "고객/클라이언트/지원자 이름",
    "datetime": "YYYY-MM-DD HH:MM 형식 (없으면 null)",
    "description": "이벤트 관련 설명"
}

한국어로 친절하고 정확하게 답변하세요."""


class EventAgent:
    """이벤트 추출 Agent (FSF 구조 재사용)"""
    
    def __init__(self):
        # 서비스는 사용 시점에 로딩 (Lazy Loading)
        pass
    
    @property
    def llm(self):
        """LLM 지연 로딩"""
        return _get_llm()
    
    @property
    def base_agent(self):
        """Agent 지연 로딩"""
        return _get_base_agent()
    
    def _get_mode_prompt(self, mode: EventType) -> str:
        """
        모드에 따른 프롬프트 추가 (Prompt Switching)
        
        Args:
            mode: 이벤트 타입
        
        Returns:
            모드별 추가 프롬프트 문자열
        """
        mode_prompts = {
            EventType.RECRUIT: "\n\n**모드: 채용 (Recruit)**\n지원자 이름과 면접 날짜/시간을 추출하세요.",
            EventType.ORDER: "\n\n**모드: 예약/주문 (Order)**\n고객 이름과 예약/픽업 날짜/시간을 추출하세요.",
            EventType.WORK: "\n\n**모드: 업무 (Work)**\n클라이언트 이름과 미팅/작업 마감일 날짜/시간을 추출하세요.",
        }
        return mode_prompts.get(mode, mode_prompts[EventType.WORK])
    
    async def analyze(
        self,
        text: str,
        mode: EventType,
        user_id: Optional[str] = None
    ) -> str:
        """
        이메일/메시지 분석 및 이벤트 정보 추출 (FSF Agent 구조 재사용)
        
        Args:
            text: 분석할 텍스트 (이메일/메시지 본문)
            mode: 이벤트 타입 (recruit/order/work)
            user_id: 사용자 ID (선택적)
        
        Returns:
            추출된 정보 (JSON 형식 문자열)
        """
        try:
            logger.info(f"🤖 Agent 분석 시작: {mode.value} - {text[:50]}...")
            
            # 모드별 프롬프트 구성
            system_prompt = REACT_AGENT_SYSTEM_PROMPT + self._get_mode_prompt(mode)
            
            # 사용자 메시지 구성
            user_message = f"다음 텍스트에서 정보를 추출해주세요:\n\n{text}"
            final_prompt = system_prompt + "\n\n사용자 요청: " + user_message
            
            # Agent 실행 (동기 함수이므로 별도 스레드에서 실행 - FSF 구조 그대로)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.base_agent.run(final_prompt)
            )
            
            logger.info(f"✅ Agent 분석 완료: {mode.value}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Agent 분석 오류: {e}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Agent 분석 실패: {str(e)}"
            )
