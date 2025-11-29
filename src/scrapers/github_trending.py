"""
GitHub Trending 스크래퍼
GitHub Trending 페이지에서 저장소 정보를 수집합니다.
"""
from bs4 import BeautifulSoup
from typing import List, Optional
import logging
from .models import TrendingRepository
from ..utils.http_client import HTTPClient

logger = logging.getLogger(__name__)


class GitHubTrendingScraper:
    """GitHub Trending 스크래퍼"""

    BASE_URL = "https://github.com/trending"

    def __init__(self):
        self.client = HTTPClient()

    def scrape(
        self,
        language: Optional[str] = None,
        since: str = "daily",
        limit: int = 25,
    ) -> List[TrendingRepository]:
        """
        GitHub Trending 저장소를 스크래핑합니다.

        Args:
            language: 프로그래밍 언어 필터 (예: 'python', 'javascript')
            since: 기간 ('daily', 'weekly', 'monthly')
            limit: 최대 저장소 수

        Returns:
            TrendingRepository 리스트
        """
        try:
            url = self.BASE_URL
            if language:
                url = f"{url}/{language.lower()}"

            params = {"since": since}

            logger.info(f"GitHub Trending 수집 시작: {url} (since={since})")
            response = self.client.get_sync(url, params=params)

            soup = BeautifulSoup(response.text, "html.parser")
            repos = self._parse_repositories(soup, limit)

            logger.info(f"총 {len(repos)}개의 저장소를 수집했습니다.")
            return repos

        except Exception as e:
            logger.error(f"GitHub Trending 스크래핑 실패: {e}")
            return []

    def _parse_repositories(
        self, soup: BeautifulSoup, limit: int
    ) -> List[TrendingRepository]:
        """저장소 목록 파싱"""
        repos = []
        articles = soup.find_all("article", class_="Box-row")[:limit]

        for article in articles:
            try:
                repo = self._parse_single_repo(article)
                if repo:
                    repos.append(repo)
            except Exception as e:
                logger.warning(f"저장소 파싱 중 오류: {e}")
                continue

        return repos

    def _parse_single_repo(self, article) -> Optional[TrendingRepository]:
        """단일 저장소 파싱"""
        try:
            # 저장소 이름과 URL
            h2 = article.find("h2", class_="h3")
            if not h2:
                return None

            link = h2.find("a")
            if not link:
                return None

            repo_path = link.get("href", "").strip("/")
            name = repo_path
            url = f"https://github.com/{repo_path}"

            # 설명
            description_elem = article.find("p", class_="col-9")
            description = (
                description_elem.get_text(strip=True) if description_elem else None
            )

            # 언어
            language = None
            language_elem = article.find("span", {"itemprop": "programmingLanguage"})
            if language_elem:
                language = language_elem.get_text(strip=True)

            # Star 수
            stars = 0
            stars_elem = article.find("svg", class_="octicon-star")
            if stars_elem and stars_elem.parent:
                stars_text = stars_elem.parent.get_text(strip=True)
                stars = self._parse_number(stars_text)

            # 오늘의 Star 증가량
            stars_today = 0
            stars_today_elem = article.find("span", class_="d-inline-block float-sm-right")
            if stars_today_elem:
                stars_today_text = stars_today_elem.get_text(strip=True)
                stars_today = self._parse_number(stars_today_text)

            # Fork 수
            forks = 0
            forks_elem = article.find("svg", class_="octicon-repo-forked")
            if forks_elem and forks_elem.parent:
                forks_text = forks_elem.parent.get_text(strip=True)
                forks = self._parse_number(forks_text)

            return TrendingRepository(
                name=name,
                description=description,
                url=url,
                language=language,
                stars=stars,
                stars_today=stars_today,
                forks=forks,
            )

        except Exception as e:
            logger.error(f"저장소 파싱 오류: {e}")
            return None

    @staticmethod
    def _parse_number(text: str) -> int:
        """숫자 파싱 (1,234 또는 1.2k 형식)"""
        try:
            text = text.replace(",", "").strip()
            if "k" in text.lower():
                return int(float(text.lower().replace("k", "")) * 1000)
            return int(text)
        except (ValueError, AttributeError):
            return 0
