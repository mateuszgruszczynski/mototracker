# All Otomoto-specific selectors live here. When Otomoto updates their layout,
# only this file needs updating.

# Search result page — listing cards
LISTING_CARD = "article[data-id]"
LISTING_ID_ATTR = "data-id"
LISTING_LINK = "h2 a[href], article a[href*='otomoto.pl/osobowe/oferta']"
LISTING_TITLE = "h2"
LISTING_PRICE = "h3"
LISTING_CURRENCY = "p:has-text('PLN'), p:has-text('EUR'), p:has-text('USD')"

# Listing card parameters (mileage, fuel, gearbox, year) — Otomoto uses <dd> elements
LISTING_PARAMS_CONTAINER = "dl"
LISTING_PARAM_ITEM = "dd"

LISTING_LOCATION = 'li:has-text("(")'  # location li contains region in parentheses
LISTING_SELLER_ID = "[data-seller-id], [data-sna-id]"

# Pagination — Otomoto uses numbered page buttons
NEXT_PAGE_LINK = (
    "a[aria-label='Next Page'], "
    "[data-testid='pagination-next'], "
    "a[rel='next'], "
    "li.pagination__item--next a"
)

# Captcha detection (page title or element when blocked)
CAPTCHA_INDICATORS = ["captcha", "robot", "challenge", "cloudflare", "access denied"]

# Otomoto base URL and search path
BASE_URL = "https://www.otomoto.pl"
SEARCH_PATH = "/osobowe"  # passenger cars

# robots.txt location
ROBOTS_URL = f"{BASE_URL}/robots.txt"

# Parameter value patterns — direct positional parsing of <dd> elements
# Otomoto <dl> inside a card has 4 <dd> in order: mileage, fuel, gearbox, year
PARAM_POSITION_MAP = {0: "mileage", 1: "fuel", 2: "gearbox", 3: "year"}
