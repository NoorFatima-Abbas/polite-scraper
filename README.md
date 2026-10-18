# polite-scraper

A small scraper for [Books to Scrape](https://books.toscrape.com), a sandbox site built for scraping practice. It downloads the first three catalogue pages, visits all 60 book pages, turns the messy HTML into clean typed records, validates every record against a schema, and ends each run with a report of what happened.

Pipeline: fetch → extract → normalize → validate → store → report

## Run it

Needs Python 3.10 or newer (developed on 3.13).

Windows (PowerShell):

```powershell
git clone https://github.com/NoorFatima-Abbas/polite-scraper.git
cd polite-scraper
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope Process RemoteSigned` first.

macOS / Linux:

```bash
git clone https://github.com/NoorFatima-Abbas/polite-scraper.git
cd polite-scraper
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

A first run makes 64 requests (1 robots.txt check, 3 catalogue pages, 60 book pages) with a one-second gap between them, so it takes roughly 1.5 to 2 minutes. It ends with a report like this:

```
--- run report ---
robots.txt status: 404
book urls found:   60
downloaded:        63 (from disk: 0)
valid records:     60
rejected:          0
duplicate upcs:    0
time:              ...
```

Pages are saved to `data/raw/` (not committed), so running again reads from disk and only re-checks robots.txt.

## Output

- `output/books.json`: the valid records
- `output/rejects.json`: pages that failed, with the URL and the reason

Each record looks like this:

```json
{
  "title": "A Light in the Attic",
  "price_gbp": 51.77,
  "stock": 22,
  "rating": 3,
  "upc": "a897fe39b1053632",
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
```

## How it behaves

**Checks before collecting.** The target is classified in [docs/TARGET.md](docs/TARGET.md): a public sandbox that invites scraping, no login, no personal data. The fetcher still reads `robots.txt` at the start of every run and obeys it. A 404 means no rules are declared; any other error status is treated as "do not crawl".

**Polite requests.** Every request carries a User-Agent that names the project and links to this repo, so the site owner can see who is calling and block or contact me. Requests are spaced one second apart. Pages already saved are never downloaded again, so a crashed run can be resumed without repeating requests.

**Nothing scraped is trusted.** Extraction raises an error when an expected field is missing rather than returning a blank. Normalization accepts only exact shapes (`£` plus digits for a price, a specific sentence for stock). Every record then has to pass the pydantic schema in `schema.py`: types are strict, unknown fields are rejected, price must be positive, rating 1 to 5, the UPC 16 hex characters, and the URL must belong to this site.

**Surviving a broken page.** Each page is handled on its own. One bad page is recorded in `rejects.json` and the run continues. The report always adds up: URLs found = valid + rejected.

## Check the schema

```
python check_schema.py
```

Feeds the schema eight deliberately bad records and shows that each one is rejected. The last line should read `unexpected acceptances: 0`.

## Files

| File | Job |
|------|-----|
| `run.py` | Runs the whole pipeline and prints the report |
| `fetcher.py` | Polite HTTP client: robots check, User-Agent, delay |
| `extract_links.py` | Pulls book URLs from a catalogue page |
| `extract_book.py` | Pulls raw fields from a book page |
| `normalize.py` | Converts strings to real types |
| `schema.py` | The contract every record must meet |
| `check_schema.py` | Proof that the schema rejects bad records |

## Limits

- Scrapes the first three catalogue pages of this one site, not all 50.
- Prices are stored as floats. Fine for display, but money arithmetic should use `Decimal` or integer pence.
- No retries: a failed request is recorded as rejected, not attempted again.
- Selectors depend on the site's current HTML. If the layout changes, extraction fails loudly instead of guessing.