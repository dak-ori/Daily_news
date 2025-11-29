"""
Slack 알림
Slack Webhook을 통해 메시지를 전송합니다.
"""
import logging
from typing import Optional
import httpx
from config.settings import settings
from ..scrapers.models import DailyDigest

logger = logging.getLogger(__name__)


class SlackNotifier:
    """Slack 알림 클라이언트"""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or settings.slack_webhook_url

        if not self.webhook_url:
            raise ValueError("Slack Webhook URL이 설정되지 않았습니다.")

    def send_daily_digest(self, digest: DailyDigest) -> bool:
        """일일 다이제스트를 Slack으로 전송"""
        try:
            date_str = digest.date.strftime("%Y년 %m월 %d일")

            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📰 Daily Tech Digest - {date_str}",
                    },
                }
            ]

            # AI 요약
            if digest.ai_daily_summary:
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*📝 오늘의 트렌드 요약*\n{digest.ai_daily_summary}",
                        },
                    }
                )
                blocks.append({"type": "divider"})

            # 주목할 기술
            if digest.ai_hot_technologies:
                tech_text = "*🔥 주목할 기술*\n"
                for tech in digest.ai_hot_technologies[:3]:
                    name = tech.get("name", "")
                    description = tech.get("description", "")
                    tech_text += f"• *{name}*: {description}\n"

                blocks.append(
                    {"type": "section", "text": {"type": "mrkdwn", "text": tech_text}}
                )
                blocks.append({"type": "divider"})

            # 트렌딩 저장소 (상위 5개)
            if digest.trending_repos:
                repo_text = "*🔥 GitHub Trending (Top 5)*\n"
                for i, repo in enumerate(digest.trending_repos[:5], 1):
                    repo_text += (
                        f"{i}. <{repo.url}|{repo.name}> "
                        f"({repo.language or 'Unknown'}) - "
                        f"⭐ {repo.stars:,} (+{repo.stars_today})\n"
                    )

                blocks.append(
                    {"type": "section", "text": {"type": "mrkdwn", "text": repo_text}}
                )

            payload = {"blocks": blocks}

            response = httpx.post(self.webhook_url, json=payload, timeout=30)
            response.raise_for_status()

            logger.info("Slack 알림 전송 완료")
            return True

        except Exception as e:
            logger.error(f"Slack 알림 전송 실패: {e}")
            return False

    def send_simple_message(self, text: str) -> bool:
        """간단한 텍스트 메시지 전송"""
        try:
            payload = {"text": text}

            response = httpx.post(self.webhook_url, json=payload, timeout=30)
            response.raise_for_status()

            logger.info("Slack 메시지 전송 완료")
            return True

        except Exception as e:
            logger.error(f"Slack 메시지 전송 실패: {e}")
            return False
