"""
OpenAI 서비스
FSF 프로젝트에서 복사 (필요한 부분만 추출)
"""
import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    """OpenAI API 서비스 래퍼"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

        self.client = OpenAI(api_key=api_key)
        self.chat_model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
        self.embedding_model = os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )

    async def generate_chat_response(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """채팅 응답 생성"""
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"OpenAI 채팅 응답 생성 오류: {e}")
            return "죄송합니다. 응답을 생성하는 중 오류가 발생했습니다."

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """텍스트 임베딩 생성"""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model, input=texts
            )
            return [data.embedding for data in response.data]

        except Exception as e:
            print(f"OpenAI 임베딩 생성 오류: {e}")
            return []

    async def generate_single_embedding(self, text: str) -> List[float]:
        """단일 텍스트 임베딩 생성"""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model, input=[text]
            )
            return response.data[0].embedding

        except Exception as e:
            print(f"OpenAI 단일 임베딩 생성 오류: {e}")
            return []

    def count_tokens(self, text: str) -> int:
        """토큰 수 계산 (대략적)"""
        return len(text) // 4
