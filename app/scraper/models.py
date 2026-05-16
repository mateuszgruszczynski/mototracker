from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ParsedListing:
    otomoto_id: str
    url: str
    title: str
    price: Decimal | None
    currency: str
    year: int | None
    mileage: int | None
    fuel: str | None
    gearbox: str | None
    location: str | None
    vin: str | None
    seller_id: str | None


class ScraperError(Exception):
    def __init__(self, details: dict):
        self.details = details
        super().__init__(str(details))
