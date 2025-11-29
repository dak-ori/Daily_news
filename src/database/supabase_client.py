"""
Supabase 클라이언트
데이터베이스 연동을 관리합니다.
"""
from supabase import create_client, Client
from typing import List, Dict, Any, Optional
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Supabase 데이터베이스 클라이언트"""

    def __init__(self):
        """Supabase 클라이언트 초기화"""
        try:
            self.client: Client = create_client(
                settings.supabase_url, settings.supabase_key
            )
            logger.info("Supabase 클라이언트 초기화 완료")
        except Exception as e:
            logger.error(f"Supabase 클라이언트 초기화 실패: {e}")
            raise

    # ==================== Trending Repos ====================

    def insert_trending_repos(self, repos: List[Dict[str, Any]]) -> bool:
        """트렌딩 저장소 삽입"""
        try:
            response = self.client.table("trending_repos").insert(repos).execute()
            logger.info(f"{len(repos)}개의 트렌딩 저장소를 저장했습니다.")
            return True
        except Exception as e:
            logger.error(f"트렌딩 저장소 저장 실패: {e}")
            return False

    def get_trending_repos(
        self, limit: int = 25, language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """트렌딩 저장소 조회"""
        try:
            query = (
                self.client.table("trending_repos")
                .select("*")
                .order("collected_at", desc=True)
                .limit(limit)
            )

            if language:
                query = query.eq("language", language)

            response = query.execute()
            return response.data
        except Exception as e:
            logger.error(f"트렌딩 저장소 조회 실패: {e}")
            return []

    def update_repo_ai_analysis(
        self, repo_id: int, ai_data: Dict[str, Any]
    ) -> bool:
        """저장소 AI 분석 결과 업데이트"""
        try:
            response = (
                self.client.table("trending_repos")
                .update(ai_data)
                .eq("id", repo_id)
                .execute()
            )
            logger.info(f"저장소 {repo_id} AI 분석 결과 업데이트 완료")
            return True
        except Exception as e:
            logger.error(f"AI 분석 결과 업데이트 실패: {e}")
            return False

    # ==================== News Articles ====================

    def insert_news_articles(self, articles: List[Dict[str, Any]]) -> bool:
        """뉴스 기사 삽입"""
        try:
            response = self.client.table("news_articles").insert(articles).execute()
            logger.info(f"{len(articles)}개의 뉴스 기사를 저장했습니다.")
            return True
        except Exception as e:
            logger.error(f"뉴스 기사 저장 실패: {e}")
            return False

    def get_news_articles(
        self, limit: int = 50, source: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """뉴스 기사 조회"""
        try:
            query = (
                self.client.table("news_articles")
                .select("*")
                .order("collected_at", desc=True)
                .limit(limit)
            )

            if source:
                query = query.eq("source", source)

            response = query.execute()
            return response.data
        except Exception as e:
            logger.error(f"뉴스 기사 조회 실패: {e}")
            return []

    # ==================== Daily Digests ====================

    def insert_or_update_daily_digest(self, digest: Dict[str, Any]) -> bool:
        """일일 다이제스트 삽입 또는 업데이트"""
        try:
            response = self.client.table("daily_digests").upsert(digest).execute()
            logger.info(f"일일 다이제스트 저장 완료: {digest.get('digest_date')}")
            return True
        except Exception as e:
            logger.error(f"일일 다이제스트 저장 실패: {e}")
            return False

    def get_daily_digest(self, date: str) -> Optional[Dict[str, Any]]:
        """특정 날짜의 다이제스트 조회"""
        try:
            response = (
                self.client.table("daily_digests")
                .select("*")
                .eq("digest_date", date)
                .execute()
            )

            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"일일 다이제스트 조회 실패: {e}")
            return None

    def get_latest_digest(self) -> Optional[Dict[str, Any]]:
        """최신 다이제스트 조회"""
        try:
            response = (
                self.client.table("daily_digests")
                .select("*")
                .order("digest_date", desc=True)
                .limit(1)
                .execute()
            )

            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"최신 다이제스트 조회 실패: {e}")
            return None

    # ==================== AI Cache ====================

    def get_cached_ai_analysis(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """캐시된 AI 분석 결과 조회 (동일 저장소명 기준)"""
        try:
            response = (
                self.client.table("trending_repos")
                .select("ai_summary, ai_use_cases, ai_difficulty, ai_related_tech")
                .eq("name", repo_name)
                .not_.is_("ai_summary", "null")
                .order("collected_at", desc=True)
                .limit(1)
                .execute()
            )

            if response.data and response.data[0].get("ai_summary"):
                logger.info(f"캐시된 AI 분석 결과 사용: {repo_name}")
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"AI 분석 캐시 조회 실패: {e}")
            return None

    def get_digests_by_date_range(
        self, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """날짜 범위로 다이제스트 조회"""
        try:
            response = (
                self.client.table("daily_digests")
                .select("*")
                .gte("digest_date", start_date)
                .lte("digest_date", end_date)
                .order("digest_date", desc=True)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"다이제스트 범위 조회 실패: {e}")
            return []

    def get_all_digest_dates(self) -> List[str]:
        """모든 다이제스트 날짜 목록 조회"""
        try:
            response = (
                self.client.table("daily_digests")
                .select("digest_date")
                .order("digest_date", desc=True)
                .execute()
            )
            return [d["digest_date"] for d in response.data]
        except Exception as e:
            logger.error(f"다이제스트 날짜 목록 조회 실패: {e}")
            return []
