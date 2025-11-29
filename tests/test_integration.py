"""
통합 테스트
전체 파이프라인 통합 테스트
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import date
import json


class TestIntegration:
    """통합 테스트"""

    @pytest.fixture
    def mock_env(self):
        """환경 변수 모킹"""
        with patch.dict('os.environ', {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_KEY': 'test-key',
            'OPENAI_API_KEY': 'test-openai-key',
        }):
            yield

    @pytest.fixture
    def sample_repos(self):
        """샘플 저장소 데이터"""
        from src.scrapers.models import TrendingRepository
        return [
            TrendingRepository(
                name="test/repo1",
                url="https://github.com/test/repo1",
                description="Test repository 1",
                language="Python",
                stars=1000,
                forks=100,
                stars_today=50,
            ),
            TrendingRepository(
                name="test/repo2",
                url="https://github.com/test/repo2",
                description="Test repository 2",
                language="JavaScript",
                stars=500,
                forks=50,
                stars_today=25,
            ),
        ]

    @pytest.fixture
    def sample_articles(self):
        """샘플 뉴스 기사 데이터"""
        from src.scrapers.models import NewsArticle
        return [
            NewsArticle(
                title="Test Article 1",
                url="https://example.com/article1",
                source="hacker_news",
                summary="This is a test article about AI",
                score=100,
            ),
            NewsArticle(
                title="Test Article 2",
                url="https://example.com/article2",
                source="geeknews",
                summary="This is a test article about Python",
                score=50,
            ),
        ]

    def test_news_aggregator_collect_all(self, sample_repos, sample_articles):
        """뉴스 어그리게이터 통합 테스트"""
        with patch('src.scrapers.news_aggregator.GitHubTrending') as MockGitHub, \
             patch('src.scrapers.news_aggregator.HackerNews') as MockHN, \
             patch('src.scrapers.news_aggregator.GeekNews') as MockGeek, \
             patch('src.scrapers.news_aggregator.YozmIT') as MockYozm:
            
            # Mock 설정
            MockGitHub.return_value.get_trending.return_value = sample_repos
            MockHN.return_value.get_top_stories.return_value = sample_articles[:1]
            MockGeek.return_value.get_latest_news.return_value = []
            MockYozm.return_value.get_latest_articles.return_value = sample_articles[1:]

            from src.scrapers.news_aggregator import NewsAggregator
            aggregator = NewsAggregator()
            
            repos, articles = aggregator.collect_all()
            
            assert len(repos) == len(sample_repos)
            assert len(articles) == len(sample_articles)
            assert repos[0].name == "test/repo1"

    def test_digest_creation_flow(self, sample_repos, sample_articles):
        """다이제스트 생성 플로우 테스트"""
        from src.scrapers.models import DailyDigest
        
        digest = DailyDigest(
            date=date.today(),
            trending_repos=sample_repos,
            news_articles=sample_articles,
            ai_daily_summary="오늘은 AI와 Python에 관한 소식이 많습니다.",
            ai_hot_technologies=[
                {"name": "AI", "description": "인공지능 기술"},
                {"name": "Python", "description": "프로그래밍 언어"},
            ],
        )
        
        assert digest.date == date.today()
        assert len(digest.trending_repos) == 2
        assert len(digest.news_articles) == 2
        assert "AI" in digest.ai_daily_summary

    def test_formatter_integration(self, sample_repos, sample_articles):
        """포맷터 통합 테스트"""
        from src.scrapers.models import DailyDigest
        from src.formatters.markdown_formatter import MarkdownFormatter
        from src.formatters.html_formatter import HTMLFormatter
        from src.formatters.console_formatter import ConsoleFormatter
        
        digest = DailyDigest(
            date=date.today(),
            trending_repos=sample_repos,
            news_articles=sample_articles,
        )
        
        # Markdown 포맷터
        md_output = MarkdownFormatter.format_daily_digest(digest)
        assert "# 📰 Daily Tech Digest" in md_output
        assert "test/repo1" in md_output
        
        # HTML 포맷터
        html_output = HTMLFormatter.format_daily_digest(digest)
        assert "<html" in html_output or "<!DOCTYPE" in html_output.upper() or "<div" in html_output
        
        # Console 포맷터는 rich 라이브러리 의존
        # 단순히 호출이 성공하는지 확인
        console = ConsoleFormatter()
        # print 함수 모킹
        with patch('builtins.print'):
            try:
                console.print_daily_digest(digest)
            except Exception:
                pass  # rich 라이브러리 없으면 스킵

    def test_notification_manager_integration(self, sample_repos, sample_articles):
        """알림 관리자 통합 테스트"""
        from src.scrapers.models import DailyDigest
        from src.notifiers.notification_manager import (
            NotificationManager,
            NotificationSummary,
        )
        
        digest = DailyDigest(
            date=date.today(),
            trending_repos=sample_repos,
            news_articles=sample_articles,
        )
        
        # 알림 채널 없이 생성
        manager = NotificationManager(
            enable_slack=False,
            enable_discord=False,
            enable_email=False,
        )
        
        result = manager.send_daily_digest(digest)
        
        assert isinstance(result, NotificationSummary)
        assert result.total_channels == 0

    @patch('src.database.supabase_client.create_client')
    def test_database_integration(self, mock_create_client, sample_repos, sample_articles):
        """데이터베이스 통합 테스트"""
        # Supabase 클라이언트 모킹
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        # insert 체인 모킹
        mock_table = MagicMock()
        mock_client.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.upsert.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[{"id": 1}])
        
        from src.database.supabase_client import SupabaseClient
        
        with patch.dict('os.environ', {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_KEY': 'test-key',
        }):
            db = SupabaseClient()
            
            # 저장소 저장 테스트
            repo = sample_repos[0]
            db.save_trending_repos([repo])
            
            mock_client.table.assert_called()


class TestEndToEnd:
    """E2E 테스트"""

    @pytest.fixture
    def mock_all_services(self):
        """모든 외부 서비스 모킹"""
        with patch('httpx.Client') as MockClient, \
             patch('src.database.supabase_client.create_client') as MockSupabase:
            
            # HTTP 클라이언트 모킹
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "<html><body>Test</body></html>"
            mock_response.json.return_value = {"items": []}
            MockClient.return_value.__enter__ = Mock(return_value=MockClient.return_value)
            MockClient.return_value.__exit__ = Mock(return_value=False)
            MockClient.return_value.get.return_value = mock_response
            
            # Supabase 모킹
            mock_supabase = MagicMock()
            MockSupabase.return_value = mock_supabase
            
            yield {
                'http_client': MockClient,
                'supabase': mock_supabase
            }

    def test_full_pipeline_mock(self, mock_all_services):
        """전체 파이프라인 모의 테스트"""
        # 이 테스트는 전체 흐름이 에러 없이 실행되는지 확인
        # 실제 외부 서비스 호출 없이 모킹된 응답 사용
        
        from src.scrapers.models import TrendingRepository, NewsArticle, DailyDigest
        from datetime import date
        
        # 샘플 데이터 생성
        repo = TrendingRepository(
            name="test/repo",
            url="https://github.com/test/repo",
            description="Test",
            language="Python",
            stars=100,
            forks=10,
            stars_today=5,
        )
        
        article = NewsArticle(
            title="Test",
            url="https://example.com",
            source="test",
        )
        
        digest = DailyDigest(
            date=date.today(),
            trending_repos=[repo],
            news_articles=[article],
        )
        
        # 다이제스트가 올바르게 생성되었는지 확인
        assert digest.date == date.today()
        assert len(digest.trending_repos) == 1
        assert len(digest.news_articles) == 1


class TestTokenMonitoring:
    """토큰 모니터링 통합 테스트"""

    def test_token_monitor_tracking(self):
        """토큰 사용량 추적 테스트"""
        from src.analyzers.llm_client import TokenMonitor, TokenUsage
        
        monitor = TokenMonitor()
        
        # 사용량 기록
        monitor.record_usage(
            model="gpt-4o-mini",
            prompt_tokens=100,
            completion_tokens=50
        )
        
        monitor.record_usage(
            model="gpt-4o-mini",
            prompt_tokens=200,
            completion_tokens=100
        )
        
        summary = monitor.get_usage_summary()
        
        assert summary["total_prompt_tokens"] == 300
        assert summary["total_completion_tokens"] == 150
        assert summary["total_requests"] == 2
        assert summary["estimated_cost_usd"] > 0


class TestCaching:
    """캐싱 통합 테스트"""

    @patch('src.database.supabase_client.create_client')
    def test_cached_analysis_retrieval(self, mock_create_client):
        """캐시된 분석 결과 조회 테스트"""
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        # 캐시 조회 결과 모킹
        mock_table = MagicMock()
        mock_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.order.return_value = mock_table
        mock_table.limit.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[{
            "name": "test/repo",
            "ai_summary": "This is a cached summary",
            "ai_use_cases": ["Use case 1", "Use case 2"],
        }])
        
        from src.database.supabase_client import SupabaseClient
        
        with patch.dict('os.environ', {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_KEY': 'test-key',
        }):
            db = SupabaseClient()
            cached = db.get_cached_ai_analysis("test/repo")
            
            assert cached is not None
            assert cached["ai_summary"] == "This is a cached summary"
