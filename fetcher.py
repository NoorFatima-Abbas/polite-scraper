import time
import urllib.robotparser

import requests


class PoliteFetcher:
    def __init__(self, base_url, user_agent, delay=1.0, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.user_agent = user_agent
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent
        self._last_request = 0.0
        self.robots_status = None
        self.robots = self._load_robots()

    def _wait(self):
        remaining = self.delay - (time.monotonic() - self._last_request)
        if remaining > 0:
            time.sleep(remaining)

    def _load_robots(self):
        self._wait()
        resp = self.session.get(f"{self.base_url}/robots.txt", timeout=self.timeout)
        self._last_request = time.monotonic()
        self.robots_status = resp.status_code
        parser = urllib.robotparser.RobotFileParser()
        if resp.status_code == 200:
            parser.parse(resp.text.splitlines())
        elif resp.status_code == 404:
            parser.allow_all = True
        else:
            parser.disallow_all = True
        return parser

    def get(self, url):
        if not self.robots.can_fetch(self.user_agent, url):
            raise PermissionError(f"robots.txt disallows {url}")
        self._wait()
        resp = self.session.get(url, timeout=self.timeout)
        self._last_request = time.monotonic()
        return resp