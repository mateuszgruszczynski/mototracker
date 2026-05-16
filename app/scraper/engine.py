import asyncio
import re
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
    LISTING_ID_ATTR,
    LISTING_LINK,
    LISTING_LOCATION,
    LISTING_PARAMS_CONTAINER,
    LISTING_PARAM_ITEM,
    LISTING_PRICE,
    LISTING_SELLER_ID,
    LISTING_TITLE,
    NEXT_PAGE_LINK,
    PARAM_LABEL_MAP,
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
    if filters.get("condition"):
        params["search[filter_enum_damaged]"] = "0"
    return f"{path}?{urlencode(params)}"


def _parse_price(text: str) -> tuple[Decimal | None, str]:
    text = text.strip()
    currency = "PLN"
    for cur in ("EUR", "USD", "PLN"):
        if cur in text:
            currency = cur
            break
    digits = re.sub(r"[^\d,.]", "", text).replace(",", ".")
    try:
        return Decimal(digits), currency
    except InvalidOperation:
        return None, currency


def _parse_params(page_content: str) -> dict[str, str]:
    return {}


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

            title_el = await card.query_selector(LISTING_TITLE)
            title = (await title_el.inner_text() if title_el else "").strip()

            price_el = await card.query_selector(LISTING_PRICE)
            price_text = (await price_el.inner_text() if price_el else "").strip()
            price, currency = _parse_price(price_text)

            location_el = await card.query_selector(LISTING_LOCATION)
            location_text = (await location_el.inner_text() if location_el else "").strip()
            location = location_text.split("\n")[0].strip() if location_text else None

            seller_el = await card.query_selector(LISTING_SELLER_ID)
            seller_id = (
                await seller_el.get_attribute("data-seller-id") or await seller_el.get_attribute("data-sna-id")
                if seller_el
                else None
            )

            params_el = await card.query_selector(LISTING_PARAMS_CONTAINER)
            year: int | None = None
            mileage: int | None = None
            fuel: str | None = None
            gearbox: str | None = None

            if params_el:
                items = await params_el.query_selector_all(LISTING_PARAM_ITEM)
                param_texts = [((await el.inner_text()).strip().lower()) for el in items]
                for i, text in enumerate(param_texts):
                    for label, field in PARAM_LABEL_MAP.items():
                        if label in text:
                            value = param_texts[i + 1] if i + 1 < len(param_texts) else text.replace(label, "").strip()
                            if field == "year":
                                m = re.search(r"\d{4}", value)
                                year = int(m.group()) if m else None
                            elif field == "mileage":
                                digits = re.sub(r"\D", "", value)
                                mileage = int(digits) if digits else None
                            elif field == "fuel":
                                fuel = value
                            elif field == "gearbox":
                                gearbox = value
                            break
                if not year and not mileage:
                    for text in param_texts:
                        m = re.match(r"^(\d{4})$", text)
                        if m:
                            year = int(m.group(1))
                        km_m = re.search(r"(\d[\d\s]+)\s*km", text)
                        if km_m:
                            mileage = int(re.sub(r"\s", "", km_m.group(1)))

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


async def scrape_search(filters: dict) -> list[ParsedListing]:
    checker = RobotsChecker(settings.scraper_user_agent)
    throttler = AsyncThrottler(settings.throttle_min_seconds, settings.throttle_jitter_seconds)
    all_listings: list[ParsedListing] = []

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
                all_listings.extend(page_listings)

                next_btn = await page.query_selector(NEXT_PAGE_LINK)
                if not next_btn:
                    break
        finally:
            await browser.close()

    return all_listings


async def check_listing_exists(url: str) -> bool:
    headers = {"User-Agent": settings.scraper_user_agent}
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.head(url, headers=headers)
            return resp.status_code != 404
    except httpx.RequestError:
        return True
