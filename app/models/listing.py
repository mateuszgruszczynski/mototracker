from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Listing(Base):
    __tablename__ = "listing"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    saved_search_id: Mapped[int] = mapped_column(Integer, ForeignKey("saved_search.id", ondelete="SET NULL"), nullable=True)
    make: Mapped[str | None] = mapped_column(String, nullable=True)
    model: Mapped[str | None] = mapped_column(String, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mileage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fuel: Mapped[str | None] = mapped_column(String, nullable=True)
    gearbox: Mapped[str | None] = mapped_column(String, nullable=True)
    vin: Mapped[str | None] = mapped_column(String, nullable=True)
    seller_id: Mapped[str | None] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    sold_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    relisted_from_listing_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("listing.id", ondelete="SET NULL"), nullable=True
    )

    price_points: Mapped[list["PricePoint"]] = relationship("PricePoint", back_populates="listing", order_by="PricePoint.observed_at")  # noqa: F821
