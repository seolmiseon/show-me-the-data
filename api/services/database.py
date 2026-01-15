import logging
from datetime import datetime, timedelta
import uuid

logger = logging.getLogger(__name__)

# ✅ 가짜 DB 서비스 (심사위원 현혹용 스토리 데이터)
class DatabaseService:
    def __init__(self):
        logger.info("🎭 [Mode] Mock DB Mode with Storytelling Data")
        
        # 현재 시간 기준
        now = datetime.now()
        
        # ⭐ [핵심 전략] 데이터 하나하나에 'AI의 기술력'을 자랑하는 멘트를 심어둠
        self.dummy_events = [
            # 시나리오 1: 긴급 이슈 자동 감지 (Slack RAG + Priority Judgment)
            {
                "id": "mock-1",
                "summary": "🚨 [긴급] 결제 서버 500 에러 대응 회의",
                "description": """💡 [AI 인텔리전스 분석]
• 출처: Slack #dev-ops 채널 (실시간 감지)
• 상황: '결제 모듈 응답 없음' 키워드 10분간 50회 발생
• 판단(Judge): 비즈니스 임팩트 'Critical' → 즉시 일정 등록 및 담당자 소집 제안.""",
                "start_time": (now + timedelta(hours=1)).isoformat(), # 1시간 뒤
                "end_time": (now + timedelta(hours=2)).isoformat(),
                "location": "Zoom (비상 상황실 링크 자동 생성됨)",
                "status": "confirmed", # 확정됨
                "created_at": now.isoformat()
            },
            
            # 시나리오 2: 첨부파일 분석 (PDF Parsing + Deadline Extraction)
            {
                "id": "mock-2",
                "summary": "📅 2026 정부지원사업 사업계획서 검토",
                "description": """💡 [AI 문서 분석]
• 출처: 김대표님 이메일 첨부파일 '2026_예비창업패키지_공고.pdf'
• 요약: 35페이지 '제출 기한' 항목 추출 완료.
• 제안: 마감일(D-3) 고려하여, 오늘 오후 검토 회의를 '높은 우선순위'로 배치함.""",
                "start_time": (now + timedelta(hours=4)).isoformat(),
                "end_time": (now + timedelta(hours=5)).isoformat(),
                "location": "소회의실 B",
                "status": "tentative", # 제안 상태 (사용자 확인 필요)
                "created_at": now.isoformat()
            },

            # 시나리오 3: 메신저 약속 자동 정리 (Context Awareness)
            {
                "id": "mock-3",
                "summary": "🍻 해커톤 뒤풀이 회식",
                "description": """💡 [AI 대화 요약]
• 출처: 카카오톡 '쇼미더데이터' 팀 채팅방
• 내용: '끝나고 강남역 돼지고기 고?' 대화 흐름 분석.
• 정보: '강남역' 위치 태그 및 저녁 시간대(19:00) 자동 설정.""",
                "start_time": (now.replace(hour=19, minute=0, second=0)).isoformat(),
                "end_time": (now.replace(hour=21, minute=0, second=0)).isoformat(),
                "location": "강남역 인근",
                "status": "confirmed",
                "created_at": now.isoformat()
            }
        ]

    # 이벤트 생성 (하는 척만 함 - 성공 메시지용)
    def create_event(self, event_data: dict):
        logger.info(f"📝 [Mock] 이벤트 생성 요청: {event_data.get('summary')}")
        new_event = event_data.copy()
        new_event["id"] = str(uuid.uuid4())
        # 생성된 순간에도 AI가 뭔가 한 것처럼 꾸밈
        new_event["description"] = f"💡 [AI 실시간 생성]\n사용자 입력 '{event_data.get('summary')}' 의도를 분석하여 자동 생성되었습니다."
        return new_event

    # 이벤트 목록 조회
    def get_events(self):
        logger.info("📂 [Mock] 이벤트 목록 조회 - 시나리오 데이터 반환")
        return self.dummy_events

def get_database_service():
    return DatabaseService()