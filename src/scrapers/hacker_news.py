"""
Hacker News 스크래퍼
Hacker News API를 사용하여 뉴스를 수집합니다.
"""
import asyncio
from typing import List, Optional
import logging
from datetime import datetime
from .models import NewsArticle
from ..utils.http_client import HTTPClient

logger = logging.getLogger(__name__)


class HackerNewsScraper:
    """Hacker News API 클라이언트"""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(self):
        self.client = HTTPClient()

    async def scrape(self, limit: int = 10) -> List[NewsArticle]:
        """
        Hacker News Top Stories를 수집합니다.

        Args:
            limit: 최대 기사 수

        Returns:
            NewsArticle 리스트
        """
        try:
            logger.info(f"Hacker News Top Stories 수집 시작 (최대 {limit}개)")

            # Top Stories ID 목록 가져오기
            top_stories_url = f"{self.BASE_URL}/topstories.json"
            response = await self.client.get(top_stories_url)
            story_ids = response.json()[:limit]

            # 각 스토리 상세 정보 가져오기
            articles = []
            tasks = [self._fetch_story(story_id) for story_id in story_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, NewsArticle):
                    articles.append(result)
                elif isinstance(result, Exception):
                    logger.warning(f"스토리 가져오기 실패: {result}")

            logger.info(f"총 {len(articles)}개의 기사를 수집했습니다.")
            return articles

        except Exception as e:
            logger.error(f"Hacker News 스크래핑 실패: {e}")
            return []

    async def _fetch_story(self, story_id: int) -> Optional[NewsArticle]:
        """단일 스토리 가져오기"""
        try:
            story_url = f"{self.BASE_URL}/item/{story_id}.json"
            response = await self.client.get(story_url)
            data = response.json()

            if not data or data.get("type") != "story":
                return None

            title = data.get("title", "")
            url = data.get("url", f"https://news.ycombinator.com/item?id={story_id}")
            score = data.get("score", 0)
            author = data.get("by", "")
            timestamp = data.get("time", 0)

            published_at = None
            if timestamp:
                published_at = datetime.fromtimestamp(timestamp)

            return NewsArticle(
                title=title,
                summary=f"Posted by {author}" if author else None,
                url=url,
                source="Hacker News",
                score=score,
                published_at=published_at,
            )

        except Exception as e:
            logger.error(f"스토리 {story_id} 가져오기 실패: {e}")
            return None

    def scrape_sync(self, limit: int = 10) -> List[NewsArticle]:
        """동기 버전의 scrape"""
        return asyncio.run(self.scrape(limit))
