from bs4 import BeautifulSoup


def _text(soup, selector, field):
    el = soup.select_one(selector)
    if el is None:
        raise ValueError(f"missing field: {field}")
    return " ".join(el.get_text().split())


def parse_book(html, url):
    soup = BeautifulSoup(html, "html.parser")

    rating_el = soup.select_one("p.star-rating")
    if rating_el is None:
        raise ValueError("missing field: rating")
    words = [c for c in rating_el.get("class", []) if c != "star-rating"]
    if not words:
        raise ValueError("missing field: rating")

    upc = None
    for row in soup.select("table.table-striped tr"):
        if row.th.get_text(strip=True) == "UPC":
            upc = row.td.get_text(strip=True)
    if upc is None:
        raise ValueError("missing field: upc")

    return {
        "title": _text(soup, "div.product_main h1", "title"),
        "price": _text(soup, "div.product_main p.price_color", "price"),
        "availability": _text(soup, "div.product_main p.availability", "availability"),
        "rating": words[0],
        "upc": upc,
        "url": url,
    }