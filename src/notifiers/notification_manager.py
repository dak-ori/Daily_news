"""
통합 알림 관리자
여러 알림 채널을 통합 관리하고 재시도 로직을 제공합니다.
"""
import time
import logging
import functools
from typing import Optional, List, Callable, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from ..scrapers.models import DailyDigest

logger = logging.getLogger(__name__)


class NotificationChannel(Enum):
    """알림 채널 종류"""
    SLACK = "slack"
    DISCORD = "discord"
    EMAIL = "email"


@dataclass
class NotificationResult:
    """알림 전송 결과"""
    channel: NotificationChannel
    success: bool
    error: Optional[str] = None
    attempts: int = 1


@dataclass
class NotificationSummary:
    """전체 알림 전송 요약"""
    total_channels: int = 0
    successful: int = 0
    failed: int = 0
    results: List[NotificationResult] = field(default_factory=list)
    
    @property
    def all_success(self) -> bool:
        return self.failed == 0 and self.successful > 0
    
    @property
    def partial_success(self) -> bool:
        return self.successful > 0 and self.failed > 0
    
    def __str__(self) -> str:
        return f"알림 전송 결과: {self.successful}/{self.total_channels} 성공"


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    재시도 데코레이터 (지수 백오프)
    
    Args:
        max_attempts: 최대 시도 횟수
        base_delay: 기본 대기 시간 (초)
        max_delay: 최대 대기 시간 (초)
        exponential_base: 지수 백오프 베이스
        exceptions: 재시도할 예외 타입들
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs), attempt
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_attempts:
                        delay = min(
                            base_delay * (exponential_base ** (attempt - 1)),
                            max_delay
                        )
                        logger.warning(
                            f"{func.__name__} 실패 (시도 {attempt}/{max_attempts}), "
                            f"{delay:.1f}초 후 재시도: {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"{func.__name__} 최종 실패 ({max_attempts}회 시도): {e}"
                        )
            
            return False, max_attempts
        
        return wrapper
    return decorator


class NotificationManager:
    """통합 알림 관리자"""
    
    def __init__(
        self,
        enable_slack: bool = False,
        enable_discord: bool = False,
        enable_email: bool = False,
        retry_attempts: int = 3,
        retry_base_delay: float = 1.0
    ):
        """
        알림 관리자 초기화
        
        Args:
            enable_slack: Slack 알림 활성화
            enable_discord: Discord 알림 활성화
            enable_email: Email 알림 활성화
            retry_attempts: 재시도 횟수
            retry_base_delay: 재시도 기본 대기 시간
        """
        self.retry_attempts = retry_attempts
        self.retry_base_delay = retry_base_delay
        self._notifiers: Dict[NotificationChannel, Any] = {}
        
        # 채널별 알림 객체 초기화
        if enable_slack:
            self._init_slack()
        if enable_discord:
            self._init_discord()
        if enable_email:
            self._init_email()
    
    def _init_slack(self):
        """Slack 알림 초기화"""
        try:
            from .slack_notifier import SlackNotifier
            self._notifiers[NotificationChannel.SLACK] = SlackNotifier()
            logger.info("✅ Slack 알림 활성화됨")
        except Exception as e:
            logger.warning(f"⚠️ Slack 알림 초기화 실패: {e}")
    
    def _init_discord(self):
        """Discord 알림 초기화"""
        try:
            from .discord_notifier import DiscordNotifier
            self._notifiers[NotificationChannel.DISCORD] = DiscordNotifier()
            logger.info("✅ Discord 알림 활성화됨")
        except Exception as e:
            logger.warning(f"⚠️ Discord 알림 초기화 실패: {e}")
    
    def _init_email(self):
        """Email 알림 초기화"""
        try:
            from .email_notifier import EmailNotifier
            self._notifiers[NotificationChannel.EMAIL] = EmailNotifier()
            logger.info("✅ Email 알림 활성화됨")
        except Exception as e:
            logger.warning(f"⚠️ Email 알림 초기화 실패: {e}")
    
    @property
    def active_channels(self) -> List[NotificationChannel]:
        """활성화된 알림 채널 목록"""
        return list(self._notifiers.keys())
    
    def _send_with_retry(
        self,
        channel: NotificationChannel,
        send_func: Callable,
        *args, **kwargs
    ) -> NotificationResult:
        """재시도 로직이 포함된 알림 전송"""
        last_error = None
        
        for attempt in range(1, self.retry_attempts + 1):
            try:
                success = send_func(*args, **kwargs)
                if success:
                    return NotificationResult(
                        channel=channel,
                        success=True,
                        attempts=attempt
                    )
                else:
                    last_error = "전송 실패 (False 반환)"
            except Exception as e:
                last_error = str(e)
            
            if attempt < self.retry_attempts:
                delay = min(
                    self.retry_base_delay * (2 ** (attempt - 1)),
                    30.0
                )
                logger.warning(
                    f"{channel.value} 알림 실패 (시도 {attempt}/{self.retry_attempts}), "
                    f"{delay:.1f}초 후 재시도"
                )
                time.sleep(delay)
        
        return NotificationResult(
            channel=channel,
            success=False,
            error=last_error,
            attempts=self.retry_attempts
        )
    
    def send_daily_digest(self, digest: DailyDigest) -> NotificationSummary:
        """
        모든 활성 채널로 일일 다이제스트 전송
        
        Args:
            digest: 전송할 DailyDigest 객체
            
        Returns:
            NotificationSummary: 전송 결과 요약
        """
        summary = NotificationSummary(total_channels=len(self._notifiers))
        
        if not self._notifiers:
            logger.warning("활성화된 알림 채널이 없습니다")
            return summary
        
        logger.info(f"📢 {len(self._notifiers)}개 채널로 알림 전송 시작")
        
        for channel, notifier in self._notifiers.items():
            logger.info(f"📤 {channel.value} 알림 전송 중...")
            
            result = self._send_with_retry(
                channel,
                notifier.send_daily_digest,
                digest
            )
            
            summary.results.append(result)
            
            if result.success:
                summary.successful += 1
                logger.info(f"✅ {channel.value} 알림 전송 완료 ({result.attempts}회 시도)")
            else:
                summary.failed += 1
                logger.error(f"❌ {channel.value} 알림 전송 실패: {result.error}")
        
        logger.info(str(summary))
        return summary
    
    def send_simple_message(self, message: str) -> NotificationSummary:
        """
        모든 활성 채널로 간단한 메시지 전송
        
        Args:
            message: 전송할 메시지
            
        Returns:
            NotificationSummary: 전송 결과 요약
        """
        summary = NotificationSummary(total_channels=len(self._notifiers))
        
        if not self._notifiers:
            logger.warning("활성화된 알림 채널이 없습니다")
            return summary
        
        for channel, notifier in self._notifiers.items():
            # 각 알림 클래스의 메시지 전송 메서드 이름이 다를 수 있음
            send_method = getattr(notifier, 'send_simple_message', None)
            if not send_method:
                send_method = getattr(notifier, 'send_message', None)
            
            if not send_method:
                logger.warning(f"{channel.value}에는 간단 메시지 전송 메서드가 없습니다")
                continue
            
            result = self._send_with_retry(channel, send_method, message)
            summary.results.append(result)
            
            if result.success:
                summary.successful += 1
            else:
                summary.failed += 1
        
        return summary
    
    def send_to_channel(
        self,
        channel: NotificationChannel,
        digest: DailyDigest
    ) -> NotificationResult:
        """
        특정 채널로만 알림 전송
        
        Args:
            channel: 전송할 채널
            digest: 전송할 DailyDigest 객체
            
        Returns:
            NotificationResult: 전송 결과
        """
        if channel not in self._notifiers:
            return NotificationResult(
                channel=channel,
                success=False,
                error=f"{channel.value} 채널이 활성화되지 않았습니다"
            )
        
        notifier = self._notifiers[channel]
        return self._send_with_retry(channel, notifier.send_daily_digest, digest)


# 편의를 위한 팩토리 함수
def create_notification_manager(
    channels: Optional[List[str]] = None,
    **kwargs
) -> NotificationManager:
    """
    알림 관리자 생성 헬퍼 함수
    
    Args:
        channels: 활성화할 채널 목록 ['slack', 'discord', 'email']
        **kwargs: NotificationManager 추가 인자
        
    Returns:
        NotificationManager 인스턴스
    """
    if channels is None:
        channels = []
    
    return NotificationManager(
        enable_slack='slack' in channels,
        enable_discord='discord' in channels,
        enable_email='email' in channels,
        **kwargs
    )
