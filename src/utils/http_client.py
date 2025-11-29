"""
HTTP 클라이언트 유틸리티
재사용 가능한 HTTP 클라이언트를 제공합니다.
"""
import httpx
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class HTTPClient:
    """HTTP 클라이언트 래퍼"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """GET 요청"""
        merged_headers = {**self.headers, **(headers or {})}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    url, params=params, headers=merged_headers, follow_redirects=True
                )
                response.raise_for_status()
                return response
            except httpx.HTTPError as e:
                logger.error(f"HTTP 요청 실패: {url} - {e}")
                raise

    def get_sync(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """동기 GET 요청"""
        merged_headers = {**self.headers, **(headers or {})}

        with httpx.Client(timeout=self.timeout) as client:
            try:
                response = client.get(
                    url, params=params, headers=merged_headers, follow_redirects=True
                )
                response.raise_for_status()
                return response
            except httpx.HTTPError as e:
                logger.error(f"HTTP 요청 실패: {url} - {e}")
                raise
