"""
Daily Tech Digest - 메인 실행 스크립트
전체 파이프라인을 실행합니다.
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional

from src.scrapers.github_trending import GitHubTrendingScraper
from src.scrapers.news_aggregator import NewsAggregator
from src.scrapers.models import DailyDigest
from src.analyzers.tech_analyzer import TechAnalyzer
from src.database.supabase_client import SupabaseClient
from src.formatters.console_formatter import ConsoleFormatter
from src.formatters.markdown_formatter import MarkdownFormatter
from src.notifiers.slack_notifier import SlackNotifier
from src.notifiers.discord_notifier import DiscordNotifier
from src.notifiers.email_notifier import EmailNotifier
from config.settings import settings

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DailyDigestPipeline:
    """일일 다이제스트 파이프라인"""

    def __init__(self):
        self.github_scraper = GitHubTrendingScraper()
        self.news_aggregator = NewsAggregator()
        # AI 분석기는 API 키가 있을 때만 초기화
        self.tech_analyzer = None
        if settings.openai_api_key or settings.anthropic_api_key or settings.google_api_key:
            try:
                provider = "google" if settings.google_api_key else ("openai" if settings.openai_api_key else "anthropic")
                self.tech_analyzer = TechAnalyzer(provider=provider)
            except Exception as e:
                logger.warning(f"AI 분석기 초기화 실패: {e}. AI 분석 없이 계속합니다.")
        self.db = SupabaseClient()

    async def run(self) -> Optional[DailyDigest]:
        """전체 파이프라인 실행"""
        try:
            logger.info("=== Daily Tech Digest 파이프라인 시작 ===")

            # 1. 데이터 수집
            logger.info("1️⃣ 데이터 수집 시작...")
            trending_repos = await asyncio.to_thread(
                self.github_scraper.scrape, limit=25
            )
            news_articles = await self.news_aggregator.collect_all(
                hn_limit=10, gn_limit=10, yozm_limit=10
            )

            logger.info(
                f"✅ 수집 완료: 저장소 {len(trending_repos)}개, 뉴스 {len(news_articles)}개"
            )

            if not trending_repos and not news_articles:
                logger.warning("수집된 데이터가 없습니다.")
                return None

            # 2. AI 분석 (상위 5개만)
            logger.info("2️⃣ AI 분석 시작...")
            if self.tech_analyzer:
                try:
                    # 트렌드 분석
                    trend_analysis = self.tech_analyzer.analyze_daily_trends(
                        trending_repos[:10], news_articles[:10]
                    )

                    # 상위 5개 저장소 상세 분석
                    for repo in trending_repos[:5]:
                        try:
                            analysis = self.tech_analyzer.analyze_repository(repo)
                            repo.ai_summary = analysis.get("ai_summary")
                            repo.ai_use_cases = analysis.get("ai_use_cases")
                            repo.ai_difficulty = analysis.get("ai_difficulty")
                            repo.ai_related_tech = analysis.get("ai_related_tech")
                        except Exception as e:
                            logger.warning(f"저장소 분석 실패: {repo.name} - {e}")

                    # 뉴스 기사 요약 (상위 10개)
                    news_articles = self.tech_analyzer.summarize_articles(
                        news_articles, max_articles=10
                    )

                    logger.info("✅ AI 분석 완료")
                except Exception as e:
                    logger.warning(f"AI 분석 실패: {e}. 분석 없이 계속합니다.")
                    trend_analysis = {}
            else:
                logger.info("⏭️  AI API 키가 없어 분석을 건너뜁니다.")
                trend_analysis = {}

            # 3. 다이제스트 생성
            logger.info("3️⃣ 다이제스트 생성...")
            digest = DailyDigest(
                date=datetime.now(),
                trending_repos=trending_repos,
                news_articles=news_articles,
                ai_daily_summary=trend_analysis.get("ai_daily_summary"),
                ai_hot_technologies=trend_analysis.get("ai_hot_technologies"),
                ai_learning_recommendations=trend_analysis.get(
                    "ai_learning_recommendations"
                ),
            )

            # 4. 데이터베이스 저장
            logger.info("4️⃣ 데이터베이스 저장...")
            try:
                # 저장소 저장 (datetime을 ISO 문자열로 변환)
                repos_data = []
                for repo in trending_repos:
                    repo_dict = repo.model_dump()
                    if repo_dict.get('collected_at'):
                        repo_dict['collected_at'] = repo_dict['collected_at'].isoformat()
                    repos_data.append(repo_dict)
                self.db.insert_trending_repos(repos_data)

                # 뉴스 저장 (datetime을 ISO 문자열로 변환)
                articles_data = []
                for article in news_articles:
                    article_dict = article.model_dump()
                    if article_dict.get('published_at'):
                        article_dict['published_at'] = article_dict['published_at'].isoformat()
                    if article_dict.get('collected_at'):
                        article_dict['collected_at'] = article_dict['collected_at'].isoformat()
                    articles_data.append(article_dict)
                self.db.insert_news_articles(articles_data)

                # 다이제스트 저장 (date를 ISO 문자열로 변환)
                digest_data = {
                    "digest_date": digest.date.date().isoformat(),
                    "top_keywords": [],
                    "ai_daily_summary": digest.ai_daily_summary,
                    "ai_hot_technologies": digest.ai_hot_technologies,
                    "ai_learning_recommendations": digest.ai_learning_recommendations,
                }
                self.db.insert_or_update_daily_digest(digest_data)

                logger.info("✅ 데이터베이스 저장 완료")
            except Exception as e:
                logger.error(f"데이터베이스 저장 실패: {e}")

            # 5. 콘솔 출력
            logger.info("5️⃣ 콘솔 출력...")
            ConsoleFormatter.print_daily_digest(digest)

            # 6. 알림 전송
            logger.info("6️⃣ 알림 전송...")
            await self._send_notifications(digest)

            # 7. 마크다운 파일 저장
            logger.info("7️⃣ 마크다운 파일 저장...")
            markdown_content = MarkdownFormatter.format_daily_digest(digest)
            filename = f"digest_{datetime.now().strftime('%Y%m%d')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            logger.info(f"✅ 마크다운 저장: {filename}")

            logger.info("=== 파이프라인 완료 ===")
            return digest

        except Exception as e:
            logger.error(f"파이프라인 실행 중 오류: {e}", exc_info=True)
            return None

    async def _send_notifications(self, digest: DailyDigest):
        """알림 전송"""
        tasks = []

        # Slack
        if settings.slack_webhook_url:
            try:
                slack = SlackNotifier()
                tasks.append(asyncio.to_thread(slack.send_daily_digest, digest))
            except Exception as e:
                logger.warning(f"Slack 초기화 실패: {e}")

        # Discord
        if settings.discord_webhook_url:
            try:
                discord = DiscordNotifier()
                tasks.append(asyncio.to_thread(discord.send_daily_digest, digest))
            except Exception as e:
                logger.warning(f"Discord 초기화 실패: {e}")

        # Email
        if settings.resend_api_key:
            try:
                email = EmailNotifier()
                tasks.append(asyncio.to_thread(email.send_daily_digest, digest))
            except Exception as e:
                logger.warning(f"Email 초기화 실패: {e}")

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"알림 전송 실패: {result}")
                elif result:
                    logger.info(f"✅ 알림 전송 완료 #{i + 1}")


async def main():
    """메인 함수"""
    pipeline = DailyDigestPipeline()
    await pipeline.run()


if __name__ == "__main__":
    asyncio.run(main())
