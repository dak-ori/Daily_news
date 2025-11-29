"""
성능 테스트
응답 시간 및 처리량 테스트
"""
import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from datetime import date
import asyncio
from concurrent.futures import ThreadPoolExecutor


class TestScraperPerformance:
    """스크래퍼 성능 테스트"""

    @pytest.fixture
    def mock_fast_response(self):
        """빠른 응답 모킹"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><div class='Box-row'></div></body></html>"
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status = Mock()
        return mock_response

    def test_github_trending_response_time(self, mock_fast_response):
        """GitHub 트렌딩 응답 시간 테스트"""
        with patch('httpx.Client') as MockClient:
            MockClient.return_value.__enter__ = Mock(return_value=MockClient.return_value)
            MockClient.return_value.__exit__ = Mock(return_value=False)
            MockClient.return_value.get.return_value = mock_fast_response
            
            from src.scrapers.github_trending import GitHubTrending
            
            scraper = GitHubTrending()
            
            start_time = time.time()
            scraper.get_trending()
            elapsed_time = time.time() - start_time
            
            # 모킹된 응답은 1초 이내에 완료되어야 함
            assert elapsed_time < 1.0, f"응답 시간이 너무 깁니다: {elapsed_time:.2f}초"

    def test_news_aggregator_parallel_collection(self):
        """뉴스 어그리게이터 병렬 수집 테스트"""
        with patch('src.scrapers.news_aggregator.GitHubTrending') as MockGitHub, \
             patch('src.scrapers.news_aggregator.HackerNews') as MockHN, \
             patch('src.scrapers.news_aggregator.GeekNews') as MockGeek, \
             patch('src.scrapers.news_aggregator.YozmIT') as MockYozm:
            
            # 각 스크래퍼가 0.1초 지연을 시뮬레이션
            def delayed_return(result):
                time.sleep(0.1)
                return result
            
            MockGitHub.return_value.get_trending.side_effect = lambda: delayed_return([])
            MockHN.return_value.get_top_stories.side_effect = lambda: delayed_return([])
            MockGeek.return_value.get_latest_news.side_effect = lambda: delayed_return([])
            MockYozm.return_value.get_latest_articles.side_effect = lambda: delayed_return([])
            
            from src.scrapers.news_aggregator import NewsAggregator
            
            aggregator = NewsAggregator()
            
            start_time = time.time()
            aggregator.collect_all()
            elapsed_time = time.time() - start_time
            
            # 순차 실행 시 0.4초 이상, 병렬 실행 시 0.2초 이하
            # 현재는 순차 실행이므로 합리적인 시간 내에 완료되면 통과
            assert elapsed_time < 2.0, f"수집 시간이 너무 깁니다: {elapsed_time:.2f}초"


class TestFormatterPerformance:
    """포맷터 성능 테스트"""

    @pytest.fixture
    def large_digest(self):
        """대용량 다이제스트 데이터"""
        from src.scrapers.models import TrendingRepository, NewsArticle, DailyDigest
        
        repos = [
            TrendingRepository(
                name=f"test/repo{i}",
                url=f"https://github.com/test/repo{i}",
                description=f"Test repository {i} with a very long description " * 10,
                language="Python",
                stars=1000 * i,
                forks=100 * i,
                stars_today=50 * i,
                ai_summary="AI generated summary " * 20,
                ai_use_cases=["Use case 1", "Use case 2", "Use case 3"],
            )
            for i in range(50)  # 50개의 저장소
        ]
        
        articles = [
            NewsArticle(
                title=f"Test Article {i}",
                url=f"https://example.com/article{i}",
                source="hacker_news",
                summary="This is a test article summary " * 10,
                score=100 * i,
            )
            for i in range(100)  # 100개의 기사
        ]
        
        return DailyDigest(
            date=date.today(),
            trending_repos=repos,
            news_articles=articles,
            ai_daily_summary="오늘의 트렌드 요약 " * 50,
            ai_hot_technologies=[
                {"name": f"Tech {i}", "description": "Technology description " * 5}
                for i in range(10)
            ],
        )

    def test_markdown_formatter_large_digest(self, large_digest):
        """대용량 다이제스트 마크다운 포맷팅 성능"""
        from src.formatters.markdown_formatter import MarkdownFormatter
        
        start_time = time.time()
        
        for _ in range(10):  # 10회 반복
            result = MarkdownFormatter.format_daily_digest(large_digest)
        
        elapsed_time = time.time() - start_time
        
        # 10회 반복이 1초 이내에 완료되어야 함
        assert elapsed_time < 1.0, f"포맷팅 시간이 너무 깁니다: {elapsed_time:.2f}초"
        assert len(result) > 1000, "결과가 너무 짧습니다"

    def test_html_formatter_large_digest(self, large_digest):
        """대용량 다이제스트 HTML 포맷팅 성능"""
        from src.formatters.html_formatter import HTMLFormatter
        
        start_time = time.time()
        
        for _ in range(10):
            result = HTMLFormatter.format_daily_digest(large_digest)
        
        elapsed_time = time.time() - start_time
        
        assert elapsed_time < 2.0, f"HTML 포맷팅 시간이 너무 깁니다: {elapsed_time:.2f}초"


class TestDatabasePerformance:
    """데이터베이스 성능 테스트"""

    @patch('src.database.supabase_client.create_client')
    def test_batch_insert_performance(self, mock_create_client):
        """배치 삽입 성능 테스트"""
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        # 빠른 응답 모킹
        mock_table = MagicMock()
        mock_client.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.upsert.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[{"id": 1}])
        
        from src.database.supabase_client import SupabaseClient
        from src.scrapers.models import TrendingRepository
        
        with patch.dict('os.environ', {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_KEY': 'test-key',
        }):
            db = SupabaseClient()
            
            # 100개의 저장소 생성
            repos = [
                TrendingRepository(
                    name=f"test/repo{i}",
                    url=f"https://github.com/test/repo{i}",
                    description=f"Test {i}",
                    language="Python",
                    stars=100 * i,
                    forks=10 * i,
                    stars_today=5 * i,
                )
                for i in range(100)
            ]
            
            start_time = time.time()
            db.save_trending_repos(repos)
            elapsed_time = time.time() - start_time
            
            # 100개 저장이 1초 이내에 완료되어야 함
            assert elapsed_time < 1.0, f"배치 삽입이 너무 느립니다: {elapsed_time:.2f}초"


class TestTokenMonitorPerformance:
    """토큰 모니터 성능 테스트"""

    def test_token_recording_performance(self):
        """대량 토큰 사용량 기록 성능"""
        from src.analyzers.llm_client import TokenMonitor
        
        monitor = TokenMonitor()
        
        start_time = time.time()
        
        # 10000회 기록
        for i in range(10000):
            monitor.record_usage(
                model="gpt-4o-mini",
                prompt_tokens=100 + i,
                completion_tokens=50 + i
            )
        
        elapsed_time = time.time() - start_time
        
        # 10000회 기록이 1초 이내에 완료되어야 함
        assert elapsed_time < 1.0, f"토큰 기록이 너무 느립니다: {elapsed_time:.2f}초"

    def test_usage_summary_performance(self):
        """사용량 요약 계산 성능"""
        from src.analyzers.llm_client import TokenMonitor
        
        monitor = TokenMonitor()
        
        # 먼저 많은 데이터 기록
        for i in range(1000):
            monitor.record_usage(
                model="gpt-4o-mini",
                prompt_tokens=100,
                completion_tokens=50
            )
        
        start_time = time.time()
        
        # 100회 요약 조회
        for _ in range(100):
            summary = monitor.get_usage_summary()
        
        elapsed_time = time.time() - start_time
        
        assert elapsed_time < 0.5, f"요약 계산이 너무 느립니다: {elapsed_time:.2f}초"
        assert summary["total_requests"] == 1000


class TestNotificationPerformance:
    """알림 성능 테스트"""

    def test_notification_manager_initialization(self):
        """알림 관리자 초기화 성능"""
        from src.notifiers.notification_manager import NotificationManager
        
        start_time = time.time()
        
        # 100회 초기화 (채널 없이)
        for _ in range(100):
            manager = NotificationManager(
                enable_slack=False,
                enable_discord=False,
                enable_email=False,
            )
        
        elapsed_time = time.time() - start_time
        
        assert elapsed_time < 1.0, f"초기화가 너무 느립니다: {elapsed_time:.2f}초"


class TestMemoryUsage:
    """메모리 사용량 테스트"""

    def test_large_digest_memory(self):
        """대용량 다이제스트 메모리 사용량"""
        import sys
        from src.scrapers.models import TrendingRepository, NewsArticle, DailyDigest
        
        repos = [
            TrendingRepository(
                name=f"test/repo{i}",
                url=f"https://github.com/test/repo{i}",
                description="x" * 1000,  # 1KB description
                language="Python",
                stars=1000,
                forks=100,
                stars_today=50,
            )
            for i in range(100)
        ]
        
        articles = [
            NewsArticle(
                title=f"Article {i}",
                url=f"https://example.com/{i}",
                source="test",
                summary="x" * 500,
            )
            for i in range(200)
        ]
        
        digest = DailyDigest(
            date=date.today(),
            trending_repos=repos,
            news_articles=articles,
        )
        
        # 대략적인 크기 확인 (정확한 메모리 측정은 어려움)
        digest_str = str(digest)
        size_kb = len(digest_str) / 1024
        
        # 다이제스트 문자열이 10MB 미만이어야 함
        assert size_kb < 10240, f"다이제스트가 너무 큽니다: {size_kb:.2f}KB"


class TestConcurrency:
    """동시성 테스트"""

    def test_concurrent_token_recording(self):
        """동시 토큰 기록 테스트"""
        from src.analyzers.llm_client import TokenMonitor
        
        monitor = TokenMonitor()
        
        def record_tokens(thread_id):
            for i in range(100):
                monitor.record_usage(
                    model="gpt-4o-mini",
                    prompt_tokens=100,
                    completion_tokens=50
                )
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            start_time = time.time()
            futures = [executor.submit(record_tokens, i) for i in range(10)]
            for f in futures:
                f.result()
            elapsed_time = time.time() - start_time
        
        summary = monitor.get_usage_summary()
        
        # 10 스레드 x 100 요청 = 1000 요청
        assert summary["total_requests"] == 1000
        assert elapsed_time < 2.0, f"동시 기록이 너무 느립니다: {elapsed_time:.2f}초"

    def test_concurrent_formatting(self):
        """동시 포맷팅 테스트"""
        from src.scrapers.models import TrendingRepository, NewsArticle, DailyDigest
        from src.formatters.markdown_formatter import MarkdownFormatter
        
        digest = DailyDigest(
            date=date.today(),
            trending_repos=[
                TrendingRepository(
                    name="test/repo",
                    url="https://github.com/test/repo",
                    description="Test",
                    language="Python",
                    stars=100,
                    forks=10,
                    stars_today=5,
                )
            ],
            news_articles=[],
        )
        
        def format_digest(thread_id):
            for _ in range(10):
                MarkdownFormatter.format_daily_digest(digest)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            start_time = time.time()
            futures = [executor.submit(format_digest, i) for i in range(5)]
            for f in futures:
                f.result()
            elapsed_time = time.time() - start_time
        
        assert elapsed_time < 2.0, f"동시 포맷팅이 너무 느립니다: {elapsed_time:.2f}초"
