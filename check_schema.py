from pydantic import ValidationError

from schema import Book

GOOD = {
    "title": "A Light in the Attic",
    "price_gbp": 51.77,
    "stock": 22,
    "rating": 3,
    "upc": "a897fe39b1053632",
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
}

CASES = {
    "negative price": {**GOOD, "price_gbp": -1.0},
    "rating out of range": {**GOOD, "rating": 6},
    "stock as string": {**GOOD, "stock": "22"},
    "bad upc": {**GOOD, "upc": "not-a-upc"},
    "empty title": {**GOOD, "title": ""},
    "extra field": {**GOOD, "isbn": "x"},
    "missing field": {k: v for k, v in GOOD.items() if k != "url"},
    "foreign url": {**GOOD, "url": "https://evil.example/catalogue/x/index.html"},
}


def main():
    Book.model_validate(GOOD)
    print("good record: accepted")
    unexpected = 0
    for name, record in CASES.items():
        try:
            Book.model_validate(record)
            print(f"{name}: ACCEPTED (should be rejected)")
            unexpected += 1
        except ValidationError:
            print(f"{name}: rejected")
    print(f"unexpected acceptances: {unexpected}")


if __name__ == "__main__":
    main()