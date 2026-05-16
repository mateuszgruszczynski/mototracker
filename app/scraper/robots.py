from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

from app.scraper.models import ScraperError


class RobotsChecker:
    def __init__(self, user_agent: str):
        self._ua = user_agent
        self._parser: RobotFileParser | None = None
        self._fetched_for_host: str | None = None

    def _ensure_fetched(self, url: str) -> None:
        parsed = urlparse(url)
        host = f"{parsed.scheme}://{parsed.netloc}"
        if self._fetched_for_host == host:
            return
        robots_url = f"{host}/robots.txt"
        try:
            resp = httpx.get(robots_url, timeout=10, headers={"User-Agent": self._ua})
            content = resp.text if resp.status_code == 200 else ""
        except httpx.RequestError:
            content = ""
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.parse(content.splitlines())
        self._parser = rp
        self._fetched_for_host = host

    def is_allowed(self, url: str) -> bool:
        self._ensure_fetched(url)
        if self._parser is None:
            return True
        return self._parser.can_fetch(self._ua, url)

    def assert_allowed(self, url: str) -> None:
        if not self.is_allowed(url):
            raise ScraperError({"code": "robots_blocked", "url": url})
