from pathlib import Path

from fetcher import PoliteFetcher

BASE_URL = "https://books.toscrape.com"
USER_AGENT = "polite-scraper/0.1 (student project; +https://github.com/NoorFatima-Abbas/polite-scraper)"
URL = f"{BASE_URL}/catalogue/a-light-in-the-attic_1000/index.html"
OUT = Path("data/raw/book-sample.html")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fetcher = PoliteFetcher(BASE_URL, USER_AGENT, delay=1.0)
    resp = fetcher.get(URL)
    resp.raise_for_status()
    OUT.write_bytes(resp.content)
    print(f"{resp.status_code} {URL} -> {OUT} ({len(resp.content)} bytes)")


if __name__ == "__main__":
    main()