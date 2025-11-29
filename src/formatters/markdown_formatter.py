"""
Markdown 포맷터
마크다운 형식으로 데이터를 포맷팅합니다.
"""
from typing import List
from datetime import datetime
from ..scrapers.models import TrendingRepository, NewsArticle, DailyDigest


class MarkdownFormatter:
    """Markdown 포맷터"""

    @staticmethod
    def format_daily_digest(digest: DailyDigest) -> str:
        """일일 다이제스트를 마크다운으로 포맷팅"""
        md_lines = []

        # 헤더
        date_str = digest.date.strftime("%Y년 %m월 %d일")
        md_lines.append(f"# 📰 Daily Tech Digest - {date_str}\n")

        # AI 요약
        if digest.ai_daily_summary:
            md_lines.append("## 📝 오늘의 트렌드 요약\n")
            md_lines.append(f"{digest.ai_daily_summary}\n")

        # 주목할 기술
        if digest.ai_hot_technologies:
            md_lines.append("## 🔥 주목할 기술\n")
            for tech in digest.ai_hot_technologies:
                name = tech.get("name", "")
                description = tech.get("description", "")
                why_hot = tech.get("why_hot", "")
                md_lines.append(f"### {name}\n")
                md_lines.append(f"{description}\n")
                if why_hot:
                    md_lines.append(f"**주목받는 이유**: {why_hot}\n")

        # 트렌딩 저장소
        if digest.trending_repos:
            md_lines.append("## 🔥 GitHub Trending\n")
            for i, repo in enumerate(digest.trending_repos[:10], 1):
                md_lines.append(
                    f"{i}. **[{repo.name}]({repo.url})** "
                    f"({repo.language or 'Unknown'}) - "
                    f"⭐ {repo.stars:,} (+{repo.stars_today})\n"
                )
                if repo.description:
                    md_lines.append(f"   {repo.description}\n")
                if repo.ai_summary:
                    md_lines.append(f"   > {repo.ai_summary}\n")

        # 뉴스 기사
        if digest.news_articles:
            md_lines.append("## 📰 IT 뉴스\n")
            for i, article in enumerate(digest.news_articles[:15], 1):
                score_str = f" ({article.score}점)" if article.score else ""
                md_lines.append(
                    f"{i}. **[{article.title}]({article.url})** "
                    f"- {article.source}{score_str}\n"
                )
                if article.summary:
                    md_lines.append(f"   {article.summary}\n")

        # 학습 추천
        if digest.ai_learning_recommendations:
            md_lines.append("## 💡 이번 주에 배워볼 만한 기술\n")
            for rec in digest.ai_learning_recommendations:
                md_lines.append(f"- {rec}\n")

        # 푸터
        md_lines.append("\n---\n")
        md_lines.append(
            f"*Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        )

        return "\n".join(md_lines)

    @staticmethod
    def format_trending_repos(repos: List[TrendingRepository]) -> str:
        """트렌딩 저장소를 마크다운으로 포맷팅"""
        md_lines = ["# 🔥 GitHub Trending Repositories\n"]

        for i, repo in enumerate(repos, 1):
            md_lines.append(
                f"{i}. **[{repo.name}]({repo.url})** "
                f"({repo.language or 'Unknown'})\n"
            )
            md_lines.append(f"   ⭐ {repo.stars:,} stars (+{repo.stars_today} today)\n")

            if repo.description:
                md_lines.append(f"   {repo.description}\n")

        return "\n".join(md_lines)

    @staticmethod
    def format_news_articles(articles: List[NewsArticle]) -> str:
        """뉴스 기사를 마크다운으로 포맷팅"""
        md_lines = ["# 📰 IT News Articles\n"]

        for i, article in enumerate(articles, 1):
            score_str = f" ({article.score}점)" if article.score else ""
            md_lines.append(
                f"{i}. **[{article.title}]({article.url})** "
                f"- {article.source}{score_str}\n"
            )

            if article.summary:
                md_lines.append(f"   {article.summary}\n")

        return "\n".join(md_lines)
