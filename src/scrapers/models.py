"""
데이터 모델 정의
Pydantic 모델을 사용하여 데이터 구조를 정의합니다.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TrendingRepository(BaseModel):
    """GitHub Trending 저장소 모델"""

    name: str = Field(..., description="저장소 이름 (owner/repo)")
    description: Optional[str] = Field(None, description="저장소 설명")
    url: str = Field(..., description="GitHub URL")
    language: Optional[str] = Field(None, description="주요 프로그래밍 언어")
    stars: int = Field(0, description="총 Star 수")
    stars_today: int = Field(0, description="오늘 증가한 Star 수")
    forks: int = Field(0, description="Fork 수")
    collected_at: datetime = Field(
        default_factory=datetime.now, description="수집 시간"
    )

    # AI 생성 필드
    ai_summary: Optional[str] = Field(None, description="AI가 생성한 기술 설명")
    ai_use_cases: Optional[List[str]] = Field(None, description="AI가 추천한 사용처 목록")
    ai_difficulty: Optional[str] = Field(None, description="학습 난이도 (초급/중급/고급)")
    ai_related_tech: Optional[List[str]] = Field(None, description="관련 기술 스택")


class NewsArticle(BaseModel):
    """뉴스 기사 모델"""

    title: str = Field(..., description="기사 제목")
    summary: Optional[str] = Field(None, description="기사 요약")
    url: str = Field(..., description="원문 URL")
    source: str = Field(..., description="뉴스 소스")
    category: Optional[str] = Field(None, description="카테고리")
    score: Optional[int] = Field(None, description="인기도 점수")
    published_at: Optional[datetime] = Field(None, description="발행일")
    collected_at: datetime = Field(
        default_factory=datetime.now, description="수집 시간"
    )


class DailyDigest(BaseModel):
    """일일 다이제스트 모델"""

    date: datetime = Field(default_factory=datetime.now, description="날짜")
    trending_repos: List[TrendingRepository] = Field(
        default_factory=list, description="트렌딩 저장소 목록"
    )
    news_articles: List[NewsArticle] = Field(
        default_factory=list, description="뉴스 기사 목록"
    )
    top_keywords: List[str] = Field(default_factory=list, description="상위 키워드")

    # AI 생성 필드
    ai_daily_summary: Optional[str] = Field(
        None, description="오늘의 기술 트렌드 종합 요약"
    )
    ai_hot_technologies: Optional[List[dict]] = Field(
        None, description="주목할 기술 + 설명 + 사용처"
    )
    ai_learning_recommendations: Optional[List[str]] = Field(
        None, description="학습 추천"
    )

    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
