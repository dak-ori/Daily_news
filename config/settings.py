"""
설정 파일
환경변수를 로드하고 관리합니다.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # Supabase
    supabase_url: str
    supabase_key: str

    # AI/LLM
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # 알림 채널
    slack_webhook_url: Optional[str] = None
    discord_webhook_url: Optional[str] = None

    # 이메일
    resend_api_key: Optional[str] = None
    email_from: Optional[str] = None
    email_to: Optional[str] = None

    # 일반 설정
    environment: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 전역 설정 인스턴스
settings = Settings()
