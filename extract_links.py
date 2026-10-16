from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/"
RAW_DIR = Path("data/raw")


def book_urls(html_path):
    html = html_path.read_bytes().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    page_url = urljoin(BASE_URL, html_path.name)
    return [urljoin(page_url, a["href"]) for a in soup.select("article.product_pod h3 a")]


def main():
    all_urls = []
    for n in range(1, 4):
        urls = book_urls(RAW_DIR / f"page-{n}.html")
        print(f"page-{n}.html: {len(urls)} urls")
        all_urls.extend(urls)
    print(f"total: {len(all_urls)}, unique: {len(set(all_urls))}")
    print(f"first: {all_urls[0]}")
    print(f"last:  {all_urls[-1]}")


if __name__ == "__main__":
    main()