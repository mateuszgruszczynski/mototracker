# i2-tasks.md — Sold Detection & Re-listing Match

## Tasks

- [x] T01 — DEV — Alembic migration: add `listing.sold_at` (DateTime, TZ-aware, nullable) and `listing.relisted_from_listing_id` (String FK → listing.id, SET NULL, nullable)
- [x] T02 — DEV — Update `Listing` ORM model with `sold_at` and `relisted_from_listing_id` fields
- [x] T03 — DEV — `app/scraper/persist.py`: after main upsert commit, re-check disappeared `active`/`likely_sold` listings via `check_listing_exists`; set `confirmed_sold`+`sold_at` on 404, `likely_sold` on reachable
- [x] T04 — DEV — `app/scraper/persist.py`: reset `likely_sold`/`confirmed_sold` → `active`, clear `sold_at` for listings re-appearing in current scan
- [x] T05 — DEV — `app/scraper/persist.py`: fuzzy match new listings against `confirmed_sold` rows (make+model+year+mileage_bucket+seller_id); set `relisted_from_listing_id` on match
