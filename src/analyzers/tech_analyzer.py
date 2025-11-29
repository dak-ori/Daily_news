"""
기술 분석기
LLM을 사용하여 기술/저장소를 분석합니다.
"""
import json
from typing import Dict, Any, List, Optional
import logging
from .llm_client import LLMClient
from ..scrapers.models import TrendingRepository
from ..database.supabase_client import SupabaseClient

logger = logging.getLogger(__name__)


class TechAnalyzer:
    """기술 분석기"""

    def __init__(self, provider: str = "openai", use_cache: bool = True):
        self.llm = LLMClient(provider=provider)
        self.use_cache = use_cache
        self._db = None
    
    @property
    def db(self) -> SupabaseClient:
        """지연 초기화된 DB 클라이언트"""
        if self._db is None:
            try:
                self._db = SupabaseClient()
            except Exception as e:
                logger.warning(f"DB 클라이언트 초기화 실패, 캐싱 비활성화: {e}")
                self.use_cache = False
        return self._db

    def analyze_repository(
        self, repo: TrendingRepository, skip_cache: bool = False
    ) -> Dict[str, Any]:
        """
        GitHub 저장소를 분석합니다.

        Args:
            repo: TrendingRepository 객체
            skip_cache: 캐시 무시 여부

        Returns:
            분석 결과 딕셔너리
        """
        try:
            # 캐시 확인
            if self.use_cache and not skip_cache:
                cached = self._get_cached_analysis(repo.name)
                if cached:
                    logger.info(f"✅ 캐시 사용: {repo.name}")
                    return cached
            
            logger.info(f"🔄 저장소 분석 시작: {repo.name}")

            prompt = self._create_analysis_prompt(repo)
            system_prompt = "당신은 기술 전문가입니다. GitHub 저장소를 분석하고 한국어로 설명해주세요."

            response = self.llm.generate(prompt, system_prompt)

            # JSON 파싱
            analysis = self._parse_analysis_response(response)

            logger.info(f"✅ 저장소 분석 완료: {repo.name}")
            return analysis

        except Exception as e:
            logger.error(f"저장소 분석 실패: {repo.name} - {e}")
            return {}
    
    def _get_cached_analysis(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """캐시된 분석 결과 조회"""
        if not self.use_cache or self.db is None:
            return None
        
        try:
            cached = self.db.get_cached_ai_analysis(repo_name)
            if cached and cached.get("ai_summary"):
                return cached
        except Exception as e:
            logger.warning(f"캐시 조회 실패: {e}")
        return None

    def _create_analysis_prompt(self, repo: TrendingRepository) -> str:
        """분석 프롬프트 생성"""
        prompt = f"""
다음 GitHub 저장소에 대해 분석해주세요.

저장소: {repo.name}
설명: {repo.description or "설명 없음"}
언어: {repo.language or "알 수 없음"}
Stars: {repo.stars:,}
오늘 증가한 Stars: {repo.stars_today}

다음 JSON 형식으로 응답해주세요:

{{
  "what_is_it": "이 기술/라이브러리가 무엇인지 2-3문장으로 설명",
  "key_features": ["특징1", "특징2", "특징3"],
  "use_cases": ["실무 활용 사례1", "활용 사례2", "활용 사례3"],
  "difficulty": "초급|중급|고급",
  "related_stack": ["관련기술1", "관련기술2", "관련기술3"]
}}

JSON만 반환하고 다른 텍스트는 포함하지 마세요.
"""
        return prompt

    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """LLM 응답 파싱"""
        try:
            # JSON 부분만 추출
            response = response.strip()

            # 마크다운 코드 블록 제거
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]

            # JSON 파싱
            data = json.loads(response)

            return {
                "ai_summary": data.get("what_is_it", ""),
                "ai_use_cases": data.get("use_cases", []),
                "ai_difficulty": data.get("difficulty", "중급"),
                "ai_related_tech": data.get("related_stack", []),
            }

        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {e}")
            return {}

    def analyze_daily_trends(
        self, repos: List[TrendingRepository], articles: List[Any]
    ) -> Dict[str, Any]:
        """
        일일 트렌드를 분석합니다.

        Args:
            repos: 트렌딩 저장소 목록
            articles: 뉴스 기사 목록

        Returns:
            일일 트렌드 분석 결과
        """
        try:
            logger.info("일일 트렌드 분석 시작")

            prompt = self._create_daily_summary_prompt(repos, articles)
            system_prompt = "당신은 기술 트렌드 분석 전문가입니다. 오늘의 기술 트렌드를 한국어로 요약해주세요."

            response = self.llm.generate(prompt, system_prompt, max_tokens=1500)

            # JSON 파싱
            analysis = self._parse_daily_summary(response)

            logger.info("일일 트렌드 분석 완료")
            return analysis

        except Exception as e:
            logger.error(f"일일 트렌드 분석 실패: {e}")
            return {}

    def _create_daily_summary_prompt(
        self, repos: List[TrendingRepository], articles: List[Any]
    ) -> str:
        """일일 요약 프롬프트 생성"""
        # 상위 10개 저장소
        top_repos = repos[:10]
        repo_list = "\n".join(
            [
                f"- {repo.name} ({repo.language}): {repo.description or '설명 없음'} - ⭐{repo.stars:,} (+{repo.stars_today})"
                for repo in top_repos
            ]
        )

        # 상위 5개 뉴스
        top_articles = articles[:5]
        article_list = "\n".join(
            [f"- {article.title} ({article.source})" for article in top_articles]
        )

        prompt = f"""
오늘의 GitHub Trending 저장소와 IT 뉴스를 기반으로 기술 트렌드를 분석해주세요.

## GitHub Trending (상위 10개)
{repo_list}

## IT 뉴스 (상위 5개)
{article_list}

다음 JSON 형식으로 응답해주세요:

{{
  "daily_summary": "오늘의 기술 트렌드를 3-4문장으로 요약",
  "hot_technologies": [
    {{"name": "기술명1", "description": "설명", "why_hot": "주목받는 이유"}},
    {{"name": "기술명2", "description": "설명", "why_hot": "주목받는 이유"}}
  ],
  "learning_recommendations": ["배워볼 만한 기술1", "배워볼 만한 기술2"]
}}

JSON만 반환하고 다른 텍스트는 포함하지 마세요.
"""
        return prompt

    def _parse_daily_summary(self, response: str) -> Dict[str, Any]:
        """일일 요약 응답 파싱"""
        try:
            # JSON 부분만 추출
            response = response.strip()

            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]

            data = json.loads(response)

            return {
                "ai_daily_summary": data.get("daily_summary", ""),
                "ai_hot_technologies": data.get("hot_technologies", []),
                "ai_learning_recommendations": data.get("learning_recommendations", []),
            }

        except json.JSONDecodeError as e:
            logger.error(f"일일 요약 JSON 파싱 실패: {e}")
            return {}

    def summarize_article(self, article) -> str:
        """
        뉴스 기사를 AI로 요약합니다.
        
        Args:
            article: NewsArticle 객체
            
        Returns:
            요약된 문자열
        """
        try:
            # 이미 요약이 있으면 그대로 반환
            if article.summary and len(article.summary) > 50:
                return article.summary
            
            prompt = f"""
다음 IT 뉴스 기사 제목을 보고 한국어로 간단히 설명해주세요 (1-2문장):

제목: {article.title}
출처: {article.source}

이 기사가 어떤 내용일지 제목을 바탕으로 추측해서 설명해주세요.
설명만 작성하고 다른 텍스트는 포함하지 마세요.
"""
            system_prompt = "당신은 IT 뉴스 전문가입니다. 기사 제목을 보고 간결하게 설명해주세요."
            
            summary = self.llm.generate(prompt, system_prompt, max_tokens=150)
            return summary.strip()
            
        except Exception as e:
            logger.error(f"기사 요약 실패: {article.title} - {e}")
            return ""

    def summarize_articles(self, articles: List, max_articles: int = 10) -> List:
        """
        여러 뉴스 기사를 요약합니다.
        
        Args:
            articles: NewsArticle 리스트
            max_articles: 최대 요약할 기사 수
            
        Returns:
            요약이 추가된 NewsArticle 리스트
        """
        logger.info(f"📰 뉴스 기사 AI 요약 시작 (최대 {max_articles}개)")
        
        for i, article in enumerate(articles[:max_articles]):
            if not article.summary or len(article.summary) < 50:
                summary = self.summarize_article(article)
                if summary:
                    article.summary = summary
                    logger.info(f"  ✅ [{i+1}/{min(len(articles), max_articles)}] {article.title[:30]}...")
        
        return articles
