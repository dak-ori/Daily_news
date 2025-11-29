"""
뉴스 통합 수집기
여러 뉴스 소스를 통합하여 관리합니다.
"""
import asyncio
from typing import List
import logging
from .models import NewsArticle
from .hacker_news import HackerNewsScraper
from .geeknews import GeekNewsScraper
from .yozm_it import YozmITScraper

logger = logging.getLogger(__name__)


class NewsAggregator:
    """뉴스 통합 수집기"""

    def __init__(self):
        self.hacker_news = HackerNewsScraper()
        self.geeknews = GeekNewsScraper()
        self.yozm_it = YozmITScraper()

    async def collect_all(
        self,
        hn_limit: int = 10,
        gn_limit: int = 10,
        yozm_limit: int = 10,
    ) -> List[NewsArticle]:
        """
        모든 소스에서 뉴스를 수집합니다.

        Args:
            hn_limit: Hacker News 기사 수
            gn_limit: GeekNews 기사 수
            yozm_limit: 요즘IT 기사 수

        Returns:
            통합된 NewsArticle 리스트
        """
        logger.info("모든 뉴스 소스에서 수집 시작")

        # 비동기로 여러 소스 수집
        tasks = [
            self.hacker_news.scrape(hn_limit),
            asyncio.to_thread(self.geeknews.scrape, gn_limit),
            asyncio.to_thread(self.yozm_it.scrape, yozm_limit),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_articles = []
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"뉴스 수집 중 오류: {result}")

        # 중복 제거
        all_articles = self._remove_duplicates(all_articles)

        logger.info(f"총 {len(all_articles)}개의 기사를 수집했습니다.")
        return all_articles

    def collect_all_sync(
        self,
        hn_limit: int = 10,
        gn_limit: int = 10,
        yozm_limit: int = 10,
    ) -> List[NewsArticle]:
        """동기 버전의 collect_all"""
        return asyncio.run(self.collect_all(hn_limit, gn_limit, yozm_limit))

    @staticmethod
    def _remove_duplicates(articles: List[NewsArticle]) -> List[NewsArticle]:
        """URL 기반으로 중복 기사 제거"""
        seen_urls = set()
        unique_articles = []

        for article in articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_articles.append(article)

        removed_count = len(articles) - len(unique_articles)
        if removed_count > 0:
            logger.info(f"{removed_count}개의 중복 기사를 제거했습니다.")

        return unique_articles
