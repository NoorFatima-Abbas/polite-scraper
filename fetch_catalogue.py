import time
from pathlib import Path

from fetcher import PoliteFetcher

BASE_URL = "https://books.toscrape.com"
USER_AGENT = "polite-scraper/0.1 (student project; +https://github.com/NoorFatima-Abbas/polite-scraper)"
RAW_DIR = Path("data/raw")


def main():
    start = time.monotonic()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fetcher = PoliteFetcher(BASE_URL, USER_AGENT, delay=1.0)
    print(f"robots.txt status: {fetcher.robots_status}")

    for n in range(1, 4):
        url = f"{BASE_URL}/catalogue/page-{n}.html"
        resp = fetcher.get(url)
        resp.raise_for_status()
        path = RAW_DIR / f"page-{n}.html"
        path.write_bytes(resp.content)
        print(f"{resp.status_code} {url} -> {path} ({len(resp.content)} bytes)")

    print(f"done in {time.monotonic() - start:.1f}s")


if __name__ == "__main__":
    main()