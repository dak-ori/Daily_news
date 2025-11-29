"""
Discord 알림
Discord Webhook을 통해 메시지를 전송합니다.
"""
import logging
import time
from typing import Optional, List
import httpx
from config.settings import settings
from ..scrapers.models import DailyDigest

logger = logging.getLogger(__name__)


class DiscordNotifier:
    """Discord 알림 클라이언트"""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or settings.discord_webhook_url

        if not self.webhook_url:
            raise ValueError("Discord Webhook URL이 설정되지 않았습니다.")

    def _send_message(self, content: str) -> bool:
        """단일 메시지 전송 (내부용)"""
        try:
            payload = {"content": content}
            response = httpx.post(self.webhook_url, json=payload, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Discord 메시지 전송 실패: {e}")
            return False

    def _send_messages(self, messages: List[str]) -> bool:
        """여러 메시지를 순차적으로 전송"""
        success = True
        for i, msg in enumerate(messages):
            if not self._send_message(msg):
                success = False
            # Discord rate limit 방지 (0.5초 대기)
            if i < len(messages) - 1:
                time.sleep(0.5)
        return success

    def send_daily_digest(self, digest: DailyDigest) -> bool:
        """일일 다이제스트를 Discord로 전송 (여러 메시지로 분할)"""
        try:
            date_str = digest.date.strftime("%Y년 %m월 %d일")
            messages = []

            # 1️⃣ 헤더 + AI 요약
            msg1 = f"# 📰 Daily Tech Digest - {date_str}\n\n"
            if digest.ai_daily_summary:
                msg1 += f"## 📝 오늘의 트렌드 요약\n{digest.ai_daily_summary}\n"
            messages.append(msg1)

            # 2️⃣ 주목할 기술
            if digest.ai_hot_technologies:
                msg2 = "## 🔥 주목할 기술\n"
                for tech in digest.ai_hot_technologies[:3]:
                    name = tech.get("name", "")
                    description = tech.get("description", "")
                    msg2 += f"• **{name}**: {description}\n"
                messages.append(msg2)

            # 3️⃣ GitHub Trending (상위 5개)
            if digest.trending_repos:
                msg3 = "## 🔥 GitHub Trending (Top 5)\n"
                for i, repo in enumerate(digest.trending_repos[:5], 1):
                    msg3 += (
                        f"{i}. **[{repo.name}](<{repo.url}>)** "
                        f"({repo.language or 'Unknown'}) - "
                        f"⭐ {repo.stars:,} (+{repo.stars_today})\n"
                    )
                    if repo.ai_summary:
                        msg3 += f"   > {repo.ai_summary}\n"
                messages.append(msg3)

            # 4️⃣ IT 뉴스 (상위 5개)
            if digest.news_articles:
                msg4 = "## 📰 IT 뉴스 (Top 5)\n"
                for i, article in enumerate(digest.news_articles[:5], 1):
                    msg4 += f"{i}. **[{article.title}](<{article.url}>)** - {article.source}"
                    if article.score:
                        msg4 += f" ({article.score}점)"
                    msg4 += "\n"
                    if article.summary and len(article.summary) > 20:
                        msg4 += f"   > {article.summary}\n"
                messages.append(msg4)

            # 메시지 전송
            result = self._send_messages(messages)
            
            if result:
                logger.info(f"Discord 알림 전송 완료 ({len(messages)}개 메시지)")
            return result

        except Exception as e:
            logger.error(f"Discord 알림 전송 실패: {e}")
            return False

    def send_simple_message(self, content: str) -> bool:
        """간단한 텍스트 메시지 전송"""
        return self._send_message(content)
