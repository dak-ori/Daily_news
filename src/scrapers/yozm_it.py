"""
요즘IT 스크래퍼
한국어 IT 뉴스를 수집합니다.
"""
from bs4 import BeautifulSoup
from typing import List
import logging
from .models import NewsArticle
from ..utils.http_client import HTTPClient

logger = logging.getLogger(__name__)


class YozmITScraper:
    """요즘IT 스크래퍼"""

    BASE_URL = "https://yozm.wishket.com"

    def __init__(self):
        self.client = HTTPClient()

    def scrape(self, limit: int = 10) -> List[NewsArticle]:
        """
        요즘IT에서 최신 뉴스를 수집합니다.

        Args:
            limit: 최대 기사 수

        Returns:
            NewsArticle 리스트
        """
        try:
            logger.info(f"요즘IT 수집 시작 (최대 {limit}개)")

            url = f"{self.BASE_URL}/magazine/list/develop/"
            response = self.client.get_sync(url)
            soup = BeautifulSoup(response.text, "html.parser")

            articles = self._parse_articles(soup, limit)

            logger.info(f"총 {len(articles)}개의 기사를 수집했습니다.")
            return articles

        except Exception as e:
            logger.error(f"요즘IT 스크래핑 실패: {e}")
            return []

    def _parse_articles(self, soup: BeautifulSoup, limit: int) -> List[NewsArticle]:
        """기사 목록 파싱"""
        articles = []

        # 요즘IT의 기사 목록 찾기
        article_elements = soup.find_all("article", class_="article-list")[:limit]

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
        title_elem = elem.find("h3") or elem.find("h2")
        if title_elem:
            link_elem = title_elem.find("a")
        else:
            link_elem = elem.find("a")

        title = title_elem.get_text(strip=True) if title_elem else ""
        link = link_elem.get("href", "") if link_elem else ""

        if link and not link.startswith("http"):
            link = f"{self.BASE_URL}{link}"

        # 요약
        summary = None
        summary_elem = elem.find("p", class_="article-summary")
        if summary_elem:
            summary = summary_elem.get_text(strip=True)

        return NewsArticle(
            title=title,
            summary=summary,
            url=link,
            source="요즘IT",
            category="IT",
        )
