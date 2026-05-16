import asyncio
import re
from collections.abc import AsyncGenerator
from decimal import Decimal, InvalidOperation
from urllib.parse import quote, urlencode

import httpx
from playwright.async_api import async_playwright, Browser, Page

from app.config import settings
from app.scraper.models import ParsedListing, ScraperError
from app.scraper.robots import RobotsChecker
from app.scraper.selectors import (
    BASE_URL,
    CAPTCHA_INDICATORS,
    LISTING_CARD,
    LISTING_CURRENCY,
    LISTING_ID_ATTR,
    LISTING_LINK,
    LISTING_LOCATION,
    LISTING_PARAM_ITEM,
    LISTING_PARAMS_CONTAINER,
    LISTING_PRICE,
    LISTING_SELLER_ID,
    LISTING_TITLE,
    NEXT_PAGE_LINK,
    PARAM_POSITION_MAP,
    SEARCH_PATH,
)
from app.scraper.throttle import AsyncThrottler


def _build_search_url(filters: dict, page: int = 1) -> str:
    make = filters.get("make", "")
    model = filters.get("model", "")

    def slugify(s: str) -> str:
        return quote(s.replace(" ", "-"), safe="-")

    path = f"{BASE_URL}{SEARCH_PATH}/{slugify(make)}/{slugify(model)}/"
    params: dict[str, str] = {"page": str(page)}
    if filters.get("year_from"):
        params["search[filter_float_year:from]"] = str(filters["year_from"])
    if filters.get("year_to"):
        params["search[filter_float_year:to]"] = str(filters["year_to"])
    if filters.get("country_of_origin"):
        params["search[filter_enum_country_origin][0]"] = filters["country_of_origin"]
    if filters.get("condition") == "nie-uszkodzony":
        params["search[filter_enum_no_accident][0]"] = "1"
    elif filters.get("condition") == "uszkodzony":
        params["search[filter_enum_no_accident][0]"] = "0"
    return f"{path}?{urlencode(params)}"


def _parse_price(text: str) -> Decimal | None:
    digits = re.sub(r"[^\d]", "", text.strip())
    try:
        return Decimal(digits) if digits else None
    except InvalidOperation:
        return None


async def _navigate_with_retry(page: Page, url: str, throttler: AsyncThrottler, max_retries: int = 2) -> None:
    await throttler.wait()
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        if attempt > 0:
            await asyncio.sleep(2 ** attempt)
        try:
            resp = await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
            status = resp.status if resp else 0
            if status in (403, 429):
                raise ScraperError({"code": "blocked", "status": status, "url": url})
            if status >= 500:
                if attempt < max_retries:
                    last_error = ScraperError({"code": "server_error", "status": status, "url": url})
                    continue
                raise ScraperError({"code": "server_error", "status": status, "url": url})
            title = await page.title()
            if any(ind in title.lower() for ind in CAPTCHA_INDICATORS):
                raise ScraperError({"code": "captcha", "url": url, "title": title})
            return
        except ScraperError:
            raise
        except Exception as exc:
            last_error = exc
            if attempt == max_retries:
                raise ScraperError({"code": "navigation_error", "url": url, "error": str(exc)}) from exc
    if last_error:
        raise last_error


async def _parse_listings_from_page(page: Page) -> list[ParsedListing]:
    cards = await page.query_selector_all(LISTING_CARD)
    listings: list[ParsedListing] = []

    for card in cards:
        try:
            otomoto_id = await card.get_attribute(LISTING_ID_ATTR) or ""
            if not otomoto_id:
                continue

            link_el = await card.query_selector(LISTING_LINK)
            url = (await link_el.get_attribute("href") if link_el else None) or ""
            if url and not url.startswith("http"):
                url = BASE_URL + url
            if not url:
                link_el2 = await card.query_selector("a[href]")
                url = (await link_el2.get_attribute("href") if link_el2 else None) or ""

            title_el = await card.query_selector(LISTING_TITLE)
            title = (await title_el.inner_text() if title_el else "").strip()

            price_el = await card.query_selector(LISTING_PRICE)
            price_text = (await price_el.inner_text() if price_el else "").strip()
            price = _parse_price(price_text)

            currency_el = await card.query_selector(LISTING_CURRENCY)
            currency = (await currency_el.inner_text() if currency_el else "PLN").strip()
            if currency not in ("PLN", "EUR", "USD"):
                currency = "PLN"

            location_el = await card.query_selector(LISTING_LOCATION)
            location_text = (await location_el.inner_text() if location_el else "").strip()
            location = location_text.split("(")[0].strip() if location_text else None

            seller_el = await card.query_selector(LISTING_SELLER_ID)
            seller_id = None
            if seller_el:
                seller_id = await seller_el.get_attribute("data-seller-id") or await seller_el.get_attribute("data-sna-id")

            params_el = await card.query_selector(LISTING_PARAMS_CONTAINER)
            year: int | None = None
            mileage: int | None = None
            fuel: str | None = None
            gearbox: str | None = None

            if params_el:
                items = await params_el.query_selector_all(LISTING_PARAM_ITEM)
                for idx, el in enumerate(items):
                    raw = (await el.inner_text()).strip()
                    field = PARAM_POSITION_MAP.get(idx)
                    if field == "mileage":
                        digits = re.sub(r"\D", "", raw)
                        mileage = int(digits) if digits else None
                    elif field == "fuel":
                        fuel = raw
                    elif field == "gearbox":
                        gearbox = raw
                    elif field == "year":
                        m = re.search(r"\d{4}", raw)
                        year = int(m.group()) if m else None

            listings.append(
                ParsedListing(
                    otomoto_id=otomoto_id,
                    url=url,
                    title=title,
                    price=price,
                    currency=currency,
                    year=year,
                    mileage=mileage,
                    fuel=fuel,
                    gearbox=gearbox,
                    location=location,
                    vin=None,
                    seller_id=seller_id,
                )
            )
        except ScraperError:
            raise
        except Exception:
            continue

    return listings


async def scrape_search(filters: dict) -> AsyncGenerator[tuple[int, list[ParsedListing]], None]:
    """Async generator yielding (page_num, page_listings) for each scraped page."""
    checker = RobotsChecker(settings.scraper_user_agent)
    throttler = AsyncThrottler(settings.throttle_min_seconds, settings.throttle_jitter_seconds)

    async with async_playwright() as pw:
        browser: Browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=settings.scraper_user_agent)
        page = await context.new_page()

        try:
            for page_num in range(1, settings.scraper_max_pages + 1):
                url = _build_search_url(filters, page=page_num)
                checker.assert_allowed(url)
                await _navigate_with_retry(page, url, throttler)

                page_listings = await _parse_listings_from_page(page)
                if not page_listings:
                    break
                yield page_num, page_listings

                next_btn = await page.query_selector(NEXT_PAGE_LINK)
                if not next_btn:
                    break
        finally:
            await browser.close()


async def check_listing_exists(url: str, throttler: AsyncThrottler | None = None) -> bool:
    if throttler is not None:
        await throttler.wait()
    headers = {"User-Agent": settings.scraper_user_agent}
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.head(url, headers=headers)
            return resp.status_code != 404
    except httpx.RequestError:
        return True
