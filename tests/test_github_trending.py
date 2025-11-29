"""
GitHub Trending 스크래퍼 테스트
"""
import pytest
from src.scrapers.github_trending import GitHubTrendingScraper


def test_scraper_initialization():
    """스크래퍼 초기화 테스트"""
    scraper = GitHubTrendingScraper()
    assert scraper is not None
    assert scraper.BASE_URL == "https://github.com/trending"


def test_scrape_daily_trending():
    """일간 트렌딩 저장소 수집 테스트"""
    scraper = GitHubTrendingScraper()
    repos = scraper.scrape(since="daily", limit=5)

    assert isinstance(repos, list)
    if len(repos) > 0:
        repo = repos[0]
        assert repo.name is not None
        assert repo.url is not None
        assert repo.url.startswith("https://github.com/")


def test_scrape_with_language_filter():
    """언어 필터링 테스트"""
    scraper = GitHubTrendingScraper()
    repos = scraper.scrape(language="python", since="daily", limit=3)

    assert isinstance(repos, list)


def test_parse_number():
    """숫자 파싱 테스트"""
    scraper = GitHubTrendingScraper()

    assert scraper._parse_number("1,234") == 1234
    assert scraper._parse_number("1.2k") == 1200
    assert scraper._parse_number("5k") == 5000
    assert scraper._parse_number("123") == 123
    assert scraper._parse_number("invalid") == 0
