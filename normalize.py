import json
import re
from collections import Counter
from pathlib import Path

from extract_book import parse_book

BOOKS_DIR = Path("data/raw/books")
CATALOGUE_URL = "https://books.toscrape.com/catalogue"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_price(text):
    match = re.fullmatch(r"£(\d+(?:\.\d{1,2})?)", text.strip())
    if not match:
        raise ValueError(f"bad price: {text!r}")
    return float(match.group(1))


def parse_stock(text):
    match = re.fullmatch(r"In stock \((\d+) available\)", text.strip())
    if not match:
        raise ValueError(f"bad availability: {text!r}")
    return int(match.group(1))


def parse_rating(word):
    if word not in RATINGS:
        raise ValueError(f"bad rating: {word!r}")
    return RATINGS[word]


def normalize(raw):
    return {
        "title": raw["title"],
        "price_gbp": parse_price(raw["price"]),
        "stock": parse_stock(raw["availability"]),
        "rating": parse_rating(raw["rating"]),
        "upc": raw["upc"],
        "url": raw["url"],
    }


def main():
    records, errors = [], []
    for path in sorted(BOOKS_DIR.glob("*.html")):
        url = f"{CATALOGUE_URL}/{path.stem}/index.html"
        try:
            html = path.read_bytes().decode("utf-8")
            records.append(normalize(parse_book(html, url)))
        except ValueError as exc:
            errors.append((path.name, str(exc)))

    for record in records[:3]:
        print(json.dumps(record, ensure_ascii=False))
    print(f"ok={len(records)} errors={len(errors)}")
    if records:
        prices = [r["price_gbp"] for r in records]
        print(f"price min={min(prices)} max={max(prices)}")
        print("ratings:", dict(sorted(Counter(r["rating"] for r in records).items())))
    for name, message in errors:
        print(f"ERROR {name}: {message}")


if __name__ == "__main__":
    main()