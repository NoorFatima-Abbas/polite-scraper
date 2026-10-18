import json
import time
from collections import Counter
from pathlib import Path

from extract_book import parse_book
from extract_links import book_urls
from fetcher import PoliteFetcher
from normalize import normalize
from schema import Book

BASE_URL = "https://books.toscrape.com"
CATALOGUE_URL = f"{BASE_URL}/catalogue"
USER_AGENT = "polite-scraper/0.1 (student project; +https://github.com/NoorFatima-Abbas/polite-scraper)"
PAGES = 3
RAW_DIR = Path("data/raw")
BOOKS_DIR = RAW_DIR / "books"
OUT_DIR = Path("output")


def slug(url):
    return url.rstrip("/").split("/")[-2]


def reason(exc):
    lines = str(exc).splitlines()
    return f"{type(exc).__name__}: {lines[0] if lines else ''}"


def fetch_cached(fetcher, url, path, counts):
    if path.exists():
        counts["cached"] += 1
        return
    resp = fetcher.get(url)
    resp.raise_for_status()
    path.write_bytes(resp.content)
    counts["fetched"] += 1
    print(f"downloaded {path.name}")


def main():
    start = time.monotonic()
    for folder in (RAW_DIR, BOOKS_DIR, OUT_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    counts = {"fetched": 0, "cached": 0}
    rejects = []
    fetcher = PoliteFetcher(BASE_URL, USER_AGENT, delay=1.0)

    urls = []
    for n in range(1, PAGES + 1):
        url = f"{CATALOGUE_URL}/page-{n}.html"
        path = RAW_DIR / f"page-{n}.html"
        try:
            fetch_cached(fetcher, url, path, counts)
            urls.extend(book_urls(path))
        except Exception as exc:
            rejects.append({"url": url, "reason": reason(exc)})

    records = []
    for url in urls:
        path = BOOKS_DIR / f"{slug(url)}.html"
        try:
            fetch_cached(fetcher, url, path, counts)
            html = path.read_bytes().decode("utf-8")
            record = Book.model_validate(normalize(parse_book(html, url))).model_dump()
            records.append(record)
        except Exception as exc:
            rejects.append({"url": url, "reason": reason(exc)})

    (OUT_DIR / "books.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT_DIR / "rejects.json").write_text(
        json.dumps(rejects, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    dupes = sum(1 for c in Counter(r["upc"] for r in records).values() if c > 1)
    print("--- run report ---")
    print(f"robots.txt status: {fetcher.robots_status}")
    print(f"book urls found:   {len(urls)}")
    print(f"downloaded:        {counts['fetched']} (from disk: {counts['cached']})")
    print(f"valid records:     {len(records)}")
    print(f"rejected:          {len(rejects)}")
    for r in rejects:
        print(f"  - {r['url']}: {r['reason']}")
    print(f"duplicate upcs:    {dupes}")
    print(f"time:              {time.monotonic() - start:.1f}s")


if __name__ == "__main__":
    main()