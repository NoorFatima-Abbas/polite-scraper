# Target classification: Books to Scrape

**Site:** https://books.toscrape.com

**What it is:** A practice site built for learning web scraping. The header says "We love being scraped!" and a banner says it is a demo site where prices and ratings are randomly assigned.

**Is scraping allowed?** Yes. That is the site's purpose.

**robots.txt:** https://books.toscrape.com/robots.txt returns 404. A missing robots.txt means no restrictions are declared, so crawling is allowed (RFC 9309). I will still request it at the start of every run and obey it if it ever appears.

**Terms or rules:** No terms page found. The only stated position is the "We love being scraped" header.

**Login and personal data:** None. All pages are public, there are no accounts, and the data is fictional.

**API:** No official API, feed or export found. Parsing the HTML is the only route. (ScraperAPI is a paid scraping service, not an API for this site.)

**Footprint:** 1 robots.txt check + 3 catalogue pages + 60 book pages = 64 requests. At a 1 second delay that is about 64 seconds plus response time. Small load for one run.

**Classification:** Public, scraping-permitted sandbox, low risk. The three habits still apply: identify myself in the User-Agent, go slowly, and treat everything scraped as untrusted input.