from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class PricePoint(Base):
    __tablename__ = "price_point"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    listing_id: Mapped[str] = mapped_column(String, ForeignKey("listing.id", ondelete="CASCADE"), nullable=False)
    scan_id: Mapped[int] = mapped_column(Integer, ForeignKey("scan.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="PLN")
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)

    listing: Mapped["Listing"] = relationship("Listing", back_populates="price_points")  # noqa: F821
    scan: Mapped["Scan"] = relationship("Scan", back_populates="price_points")  # noqa: F821
