import time
from pathlib import Path

from extract_links import RAW_DIR, book_urls
from fetcher import PoliteFetcher

BASE_URL = "https://books.toscrape.com"
USER_AGENT = "polite-scraper/0.1 (student project; +https://github.com/NoorFatima-Abbas/polite-scraper)"
BOOKS_DIR = RAW_DIR / "books"


def slug(url):
    return url.rstrip("/").split("/")[-2]


def main():
    start = time.monotonic()
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)

    urls = []
    for n in range(1, 4):
        urls.extend(book_urls(RAW_DIR / f"page-{n}.html"))

    fetcher = PoliteFetcher(BASE_URL, USER_AGENT, delay=1.0)
    fetched = skipped = failed = 0

    for i, url in enumerate(urls, 1):
        path = BOOKS_DIR / f"{slug(url)}.html"
        if path.exists():
            skipped += 1
            continue
        try:
            resp = fetcher.get(url)
            resp.raise_for_status()
            path.write_bytes(resp.content)
            fetched += 1
            print(f"[{i}/{len(urls)}] {resp.status_code} {path.name}")
        except Exception as exc:
            failed += 1
            print(f"[{i}/{len(urls)}] FAILED {url}: {exc}")

    print(f"fetched={fetched} skipped={skipped} failed={failed} in {time.monotonic() - start:.1f}s")


if __name__ == "__main__":
    main()