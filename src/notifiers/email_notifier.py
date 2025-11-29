"""
이메일 알림
Resend API를 통해 이메일을 전송합니다.
"""
import logging
from typing import Optional
from config.settings import settings
from ..scrapers.models import DailyDigest
from ..formatters.html_formatter import HTMLFormatter

logger = logging.getLogger(__name__)


class EmailNotifier:
    """이메일 알림 클라이언트"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        from_email: Optional[str] = None,
        to_email: Optional[str] = None,
    ):
        self.api_key = api_key or settings.resend_api_key
        self.from_email = from_email or settings.email_from
        self.to_email = to_email or settings.email_to

        if not self.api_key:
            raise ValueError("Resend API Key가 설정되지 않았습니다.")

        if not self.from_email or not self.to_email:
            raise ValueError("이메일 주소가 설정되지 않았습니다.")

    def send_daily_digest(self, digest: DailyDigest) -> bool:
        """일일 다이제스트를 이메일로 전송"""
        try:
            import resend

            resend.api_key = self.api_key

            date_str = digest.date.strftime("%Y년 %m월 %d일")
            subject = f"📰 Daily Tech Digest - {date_str}"

            # HTML 포맷팅
            html_content = HTMLFormatter.format_daily_digest(digest)

            params = {
                "from": self.from_email,
                "to": [self.to_email],
                "subject": subject,
                "html": html_content,
            }

            resend.Emails.send(params)

            logger.info(f"이메일 전송 완료: {self.to_email}")
            return True

        except Exception as e:
            logger.error(f"이메일 전송 실패: {e}")
            return False
