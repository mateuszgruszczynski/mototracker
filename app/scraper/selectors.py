# All Otomoto-specific selectors live here. When Otomoto updates their layout,
# only this file needs updating.

# Search result page — listing cards
LISTING_CARD = "article[data-id]"
LISTING_ID_ATTR = "data-id"
LISTING_LINK = "h2 a[href], a.ooa-1n2s58e[href], article a[href]"
LISTING_TITLE = "h2"
LISTING_PRICE = "[data-testid='ad-price'], .ooa-1bmnv3, span[class*='price']"
LISTING_CURRENCY = LISTING_PRICE  # currency text is adjacent to price number

# Listing card parameters (year, mileage, fuel, gearbox)
LISTING_PARAMS_CONTAINER = "ul[class*='params'], dl[class*='params']"
LISTING_PARAM_ITEM = "li, dd"

LISTING_LOCATION = "[class*='location'], [data-testid='location-date']"
LISTING_SELLER_ID = "[data-seller-id], [data-sna-id]"

# Pagination
NEXT_PAGE_LINK = "a[data-testid='pagination-next'], a[aria-label='Next Page'], li.next a"

# Captcha detection (page title or element when blocked)
CAPTCHA_INDICATORS = ["captcha", "robot", "challenge", "cloudflare"]

# Otomoto base URL and search path
BASE_URL = "https://www.otomoto.pl"
SEARCH_PATH = "/osobowe"  # passenger cars

# robots.txt location
ROBOTS_URL = f"{BASE_URL}/robots.txt"

# Known Otomoto parameter labels (Polish) → field mapping
PARAM_LABEL_MAP: dict[str, str] = {
    "rok produkcji": "year",
    "przebieg": "mileage",
    "rodzaj paliwa": "fuel",
    "skrzynia biegów": "gearbox",
}
