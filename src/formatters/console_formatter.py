"""
콘솔 포맷터
터미널에 예쁘게 출력합니다.
"""
from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from ..scrapers.models import TrendingRepository, NewsArticle, DailyDigest

console = Console()


class ConsoleFormatter:
    """콘솔 출력 포맷터"""

    @staticmethod
    def print_trending_repos(repos: List[TrendingRepository]):
        """트렌딩 저장소 출력"""
        table = Table(title="🔥 GitHub Trending Repositories", show_lines=True)

        table.add_column("Repository", style="cyan", no_wrap=True)
        table.add_column("Language", style="magenta")
        table.add_column("Stars", justify="right", style="green")
        table.add_column("Today", justify="right", style="yellow")
        table.add_column("Description", style="white")

        for repo in repos:
            table.add_row(
                repo.name,
                repo.language or "-",
                f"{repo.stars:,}",
                f"+{repo.stars_today}",
                (repo.description or "")[:60] + "..." if repo.description and len(repo.description) > 60 else (repo.description or "-"),
            )

        console.print(table)

    @staticmethod
    def print_news_articles(articles: List[NewsArticle]):
        """뉴스 기사 출력"""
        table = Table(title="📰 IT News Articles", show_lines=True)

        table.add_column("Source", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Score", justify="right", style="yellow")

        for article in articles:
            table.add_row(
                article.source,
                article.title[:80] + "..." if len(article.title) > 80 else article.title,
                str(article.score) if article.score else "-",
            )

        console.print(table)

    @staticmethod
    def print_daily_digest(digest: DailyDigest):
        """일일 다이제스트 출력"""
        console.print(
            Panel(
                f"[bold cyan]Daily Tech Digest[/bold cyan]\n"
                f"[white]{digest.date.strftime('%Y-%m-%d')}[/white]",
                border_style="blue",
            )
        )

        # AI 요약
        if digest.ai_daily_summary:
            console.print("\n📝 [bold yellow]오늘의 트렌드 요약[/bold yellow]")
            console.print(digest.ai_daily_summary)

        # 주목할 기술
        if digest.ai_hot_technologies:
            console.print("\n🔥 [bold red]주목할 기술[/bold red]")
            for tech in digest.ai_hot_technologies:
                console.print(
                    f"  • [cyan]{tech.get('name', '')}[/cyan]: {tech.get('description', '')}"
                )

        # 학습 추천
        if digest.ai_learning_recommendations:
            console.print("\n💡 [bold green]학습 추천[/bold green]")
            for rec in digest.ai_learning_recommendations:
                console.print(f"  • {rec}")

        console.print()
