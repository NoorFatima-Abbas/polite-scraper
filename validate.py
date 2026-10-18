from collections import Counter

from pydantic import ValidationError

from extract_book import parse_book
from normalize import BOOKS_DIR, CATALOGUE_URL, normalize
from schema import Book


def validate_record(record):
    return Book.model_validate(record).model_dump()


def main():
    valid, invalid = [], []
    for path in sorted(BOOKS_DIR.glob("*.html")):
        url = f"{CATALOGUE_URL}/{path.stem}/index.html"
        try:
            html = path.read_bytes().decode("utf-8")
            valid.append(validate_record(normalize(parse_book(html, url))))
        except (ValueError, ValidationError) as exc:
            invalid.append((path.name, str(exc).splitlines()[0]))

    dupes = [u for u, c in Counter(r["upc"] for r in valid).items() if c > 1]
    print(f"valid={len(valid)} invalid={len(invalid)} duplicate_upcs={len(dupes)}")
    for name, message in invalid:
        print(f"INVALID {name}: {message}")


if __name__ == "__main__":
    main()