"""
HTML 포맷터
HTML 이메일 템플릿을 생성합니다.
"""
from typing import List
from datetime import datetime
from ..scrapers.models import TrendingRepository, NewsArticle, DailyDigest


class HTMLFormatter:
    """HTML 포맷터"""

    @staticmethod
    def format_daily_digest(digest: DailyDigest) -> str:
        """일일 다이제스트를 HTML로 포맷팅"""
        date_str = digest.date.strftime("%Y년 %m월 %d일")

        html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Tech Digest - {date_str}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .summary {{
            background-color: #ecf0f1;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 20px 0;
        }}
        .repo-item, .news-item {{
            margin: 20px 0;
            padding: 15px;
            border-left: 3px solid #e0e0e0;
            background-color: #fafafa;
        }}
        .repo-item h3, .news-item h3 {{
            margin: 0 0 10px 0;
            color: #2980b9;
        }}
        .meta {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .tech-item {{
            margin: 15px 0;
            padding: 15px;
            background-color: #fff3cd;
            border-left: 3px solid #ffc107;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 Daily Tech Digest</h1>
        <p class="meta">{date_str}</p>
        """

        # AI 요약
        if digest.ai_daily_summary:
            html += f"""
        <div class="summary">
            <h2>📝 오늘의 트렌드 요약</h2>
            <p>{digest.ai_daily_summary}</p>
        </div>
        """

        # 주목할 기술
        if digest.ai_hot_technologies:
            html += "<h2>🔥 주목할 기술</h2>"
            for tech in digest.ai_hot_technologies:
                name = tech.get("name", "")
                description = tech.get("description", "")
                why_hot = tech.get("why_hot", "")
                html += f"""
        <div class="tech-item">
            <h3>{name}</h3>
            <p>{description}</p>
            {f'<p><strong>주목받는 이유:</strong> {why_hot}</p>' if why_hot else ''}
        </div>
        """

        # 트렌딩 저장소
        if digest.trending_repos:
            html += "<h2>🔥 GitHub Trending</h2>"
            for repo in digest.trending_repos[:10]:
                html += f"""
        <div class="repo-item">
            <h3><a href="{repo.url}" target="_blank">{repo.name}</a></h3>
            <p class="meta">{repo.language or 'Unknown'} • ⭐ {repo.stars:,} (+{repo.stars_today})</p>
            {f'<p>{repo.description}</p>' if repo.description else ''}
            {f'<p><em>{repo.ai_summary}</em></p>' if repo.ai_summary else ''}
        </div>
        """

        # 뉴스 기사
        if digest.news_articles:
            html += "<h2>📰 IT 뉴스</h2>"
            for article in digest.news_articles[:15]:
                score_str = f" • {article.score}점" if article.score else ""
                html += f"""
        <div class="news-item">
            <h3><a href="{article.url}" target="_blank">{article.title}</a></h3>
            <p class="meta">{article.source}{score_str}</p>
            {f'<p>{article.summary}</p>' if article.summary else ''}
        </div>
        """

        # 학습 추천
        if digest.ai_learning_recommendations:
            html += "<h2>💡 이번 주에 배워볼 만한 기술</h2><ul>"
            for rec in digest.ai_learning_recommendations:
                html += f"<li>{rec}</li>"
            html += "</ul>"

        # 푸터
        html += f"""
        <div class="footer">
            <p>Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        return html
