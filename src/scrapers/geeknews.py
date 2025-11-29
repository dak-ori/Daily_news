"""
GeekNews 스크래퍼
한국어 기술 뉴스를 수집합니다.
"""
from bs4 import BeautifulSoup
from typing import List
import logging
from datetime import datetime
from .models import NewsArticle
from ..utils.http_client import HTTPClient

logger = logging.getLogger(__name__)


class GeekNewsScraper:
    """GeekNews 스크래퍼"""

    BASE_URL = "https://news.hada.io"

    def __init__(self):
        self.client = HTTPClient()

    def scrape(self, limit: int = 10) -> List[NewsArticle]:
        """
        GeekNews에서 최신 뉴스를 수집합니다.

        Args:
            limit: 최대 기사 수

        Returns:
            NewsArticle 리스트
        """
        try:
            logger.info(f"GeekNews 수집 시작 (최대 {limit}개)")

            response = self.client.get_sync(self.BASE_URL)
            soup = BeautifulSoup(response.text, "html.parser")

            articles = self._parse_articles(soup, limit)

            logger.info(f"총 {len(articles)}개의 기사를 수집했습니다.")
            return articles

        except Exception as e:
            logger.error(f"GeekNews 스크래핑 실패: {e}")
            return []

    def _parse_articles(self, soup: BeautifulSoup, limit: int) -> List[NewsArticle]:
        """기사 목록 파싱"""
        articles = []

        # GeekNews의 기사 목록 찾기
        # 실제 HTML 구조에 맞춰 셀렉터를 조정해야 할 수 있습니다
        article_elements = soup.find_all("div", class_="topic_row")[:limit]

        for elem in article_elements:
            try:
                article = self._parse_single_article(elem)
                if article:
                    articles.append(article)
            except Exception as e:
                logger.warning(f"기사 파싱 중 오류: {e}")
                continue

        return articles

    def _parse_single_article(self, elem) -> NewsArticle:
        """단일 기사 파싱"""
        # 제목과 링크
        title_elem = elem.find("h1", class_="topictitle")
        if not title_elem:
            title_elem = elem.find("a", class_="topic_link")

        title = title_elem.get_text(strip=True) if title_elem else ""

        link = title_elem.get("href", "") if title_elem else ""
        if link and not link.startswith("http"):
            link = f"{self.BASE_URL}{link}"

        # 점수
        score = 0
        score_elem = elem.find("span", class_="topicvotecount")
        if score_elem:
            try:
                score = int(score_elem.get_text(strip=True))
            except (ValueError, AttributeError):
                score = 0

        return NewsArticle(
            title=title,
            url=link,
            source="GeekNews",
            score=score,
            category="Tech",
        )
