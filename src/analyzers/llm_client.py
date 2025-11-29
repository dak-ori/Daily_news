"""
LLM 클라이언트
다양한 LLM API를 통합하여 관리합니다.
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class TokenUsage:
    """토큰 사용량 추적"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    model: str = ""
    provider: str = ""


class TokenMonitor:
    """토큰 사용량 모니터링"""
    
    # 모델별 가격 (1K 토큰당 USD)
    PRICING = {
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
        "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
        "gemini-2.5-flash": {"input": 0.0, "output": 0.0},  # 무료 티어
    }
    
    def __init__(self):
        self.usage_history: list[TokenUsage] = []
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0
    
    def record_usage(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        model: str,
        provider: str
    ) -> TokenUsage:
        """토큰 사용량 기록"""
        total = prompt_tokens + completion_tokens
        
        # 비용 계산
        pricing = self.PRICING.get(model, {"input": 0, "output": 0})
        cost = (prompt_tokens / 1000 * pricing["input"]) + \
               (completion_tokens / 1000 * pricing["output"])
        
        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total,
            estimated_cost=cost,
            model=model,
            provider=provider
        )
        
        self.usage_history.append(usage)
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_cost += cost
        
        logger.info(
            f"📊 토큰 사용: {prompt_tokens}+{completion_tokens}={total} "
            f"(${cost:.6f}) | 누적: {self.total_prompt_tokens}+{self.total_completion_tokens} "
            f"(${self.total_cost:.6f})"
        )
        
        return usage
    
    def get_summary(self) -> Dict[str, Any]:
        """사용량 요약"""
        return {
            "total_requests": len(self.usage_history),
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
            "total_cost_usd": round(self.total_cost, 6),
        }


class LLMClient:
    """LLM API 클라이언트"""
    
    # 전역 토큰 모니터
    token_monitor = TokenMonitor()

    def __init__(self, provider: str = "openai"):
        """
        LLM 클라이언트 초기화

        Args:
            provider: 'openai', 'anthropic', 'google' 중 선택
        """
        self.provider = provider
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        """선택한 provider의 클라이언트 초기화"""
        if self.provider == "openai":
            self._initialize_openai()
        elif self.provider == "anthropic":
            self._initialize_anthropic()
        elif self.provider == "google":
            self._initialize_google()
        else:
            raise ValueError(f"지원하지 않는 provider: {self.provider}")

    def _initialize_openai(self):
        """OpenAI 클라이언트 초기화"""
        try:
            from openai import OpenAI

            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

            self._client = OpenAI(api_key=settings.openai_api_key)
            logger.info("OpenAI 클라이언트 초기화 완료")
        except Exception as e:
            logger.error(f"OpenAI 클라이언트 초기화 실패: {e}")
            raise

    def _initialize_anthropic(self):
        """Anthropic 클라이언트 초기화"""
        try:
            from anthropic import Anthropic

            if not settings.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")

            self._client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("Anthropic 클라이언트 초기화 완료")
        except Exception as e:
            logger.error(f"Anthropic 클라이언트 초기화 실패: {e}")
            raise

    def _initialize_google(self):
        """Google Gemini 클라이언트 초기화"""
        try:
            import google.generativeai as genai

            if not settings.google_api_key:
                raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")

            genai.configure(api_key=settings.google_api_key)
            # gemini-2.5-flash 사용 (최신 모델)
            self._client = genai.GenerativeModel("models/gemini-2.5-flash")
            logger.info("Google Gemini 2.5 Flash 클라이언트 초기화 완료")
        except Exception as e:
            logger.error(f"Google Gemini 클라이언트 초기화 실패: {e}")
            raise

    def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> str:
        """텍스트 생성"""
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt, system_prompt, **kwargs)
            elif self.provider == "anthropic":
                return self._generate_anthropic(prompt, system_prompt, **kwargs)
            elif self.provider == "google":
                return self._generate_google(prompt, system_prompt, **kwargs)
        except Exception as e:
            logger.error(f"텍스트 생성 실패: {e}")
            raise

    def _generate_openai(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> str:
        """OpenAI로 텍스트 생성"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        model = kwargs.get("model", "gpt-4o-mini")
        response = self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1000),
        )

        # 토큰 사용량 기록
        if response.usage:
            self.token_monitor.record_usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                model=model,
                provider="openai"
            )

        return response.choices[0].message.content

    def _generate_anthropic(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> str:
        """Anthropic으로 텍스트 생성"""
        model = kwargs.get("model", "claude-3-haiku-20240307")
        response = self._client.messages.create(
            model=model,
            max_tokens=kwargs.get("max_tokens", 1000),
            temperature=kwargs.get("temperature", 0.7),
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}],
        )

        # 토큰 사용량 기록
        if response.usage:
            self.token_monitor.record_usage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                model=model,
                provider="anthropic"
            )

        return response.content[0].text

    def _generate_google(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> str:
        """Google Gemini로 텍스트 생성"""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = self._client.generate_content(full_prompt)
        
        # Gemini 토큰 사용량 기록 (추정치)
        # Gemini는 무료 티어이므로 대략적인 토큰 수만 추정
        prompt_tokens = len(full_prompt.split()) * 1.3  # 대략적 추정
        completion_tokens = len(response.text.split()) * 1.3 if response.text else 0
        self.token_monitor.record_usage(
            prompt_tokens=int(prompt_tokens),
            completion_tokens=int(completion_tokens),
            model="gemini-2.5-flash",
            provider="google"
        )
        
        return response.text
    
    @classmethod
    def get_usage_summary(cls) -> Dict[str, Any]:
        """전역 토큰 사용량 요약 조회"""
        return cls.token_monitor.get_summary()
