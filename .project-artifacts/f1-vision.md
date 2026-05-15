# Vision — MotoTracker

## Vision Statement
A local, on-demand price tracker for cars listed on Otomoto.pl. The user defines saved searches (make, model, year range, etc.); each scan records every matching listing's price and timestamp. Re-scans append new price points to known cars and flag listings that have disappeared, surfacing price-change history and likely-sold signals over time.

## Target user
- Single user: the owner. Local-only deployment.

## App type and platform(s)
- Local web app (browser UI talking to a local backend on the same machine).
- Stack chosen in Architecture phase (no user preference).

## Hard constraints
- Target portal: Otomoto.pl (Polish car marketplace).
- Local-only; no public hosting, no multi-user auth.
- Must respect Otomoto's bot/rate limits (be polite — throttled scraping).

## Out of scope
- Multi-user / public deployment.
- Scheduled / cron-driven scans (manual on-demand only in v1).
- Other portals (OLX, Allegro, mobile.de).
- Notifications (email/push).
- Buying/selling actions.

## Success criteria
- I can save a car search and re-run it any time.
- After two+ scans of the same search, I can see price-change history per car.
- I can tell which cars from a search are still active vs likely sold.

## Key user journey
1. Open the app, create a saved search: `Make=BMW, Model=Seria 3, Year=2015–2020, Country of origin=Poland, Condition=not damaged`.
2. Click "Run scan". App fetches results from Otomoto, persists each listing's metadata + price + scan timestamp.
3. Days later, click "Run scan" again on the same saved search.
   - Listings still present: a new price-point row is appended (or unchanged-price marker).
   - Listings no longer present: app re-fetches their detail page; if gone, marks them `likely sold/withdrawn`.
4. Open a car's detail page → see full metadata + price-history chart + current status.
5. Open the search's results page → see the latest scan as a table with price-change badges.

## Identity & sold detection
- Primary match: Otomoto listing ID/URL.
- Fuzzy fallback: VIN if available, else (make + model + year + mileage + seller) to catch re-listings.
- Sold/withdrawn: disappearance from results triggers a detail-page re-check; both signals combined confirm.

## Filters supported in v1
- Make, model
- Year range (from–to)
- Country of origin = Poland
- Condition = not damaged

## MVP
- Create / list saved searches with the v1 filters above.
- Run a scan on demand against Otomoto; persist listings + price + timestamp.
- Re-scan: dedupe by Otomoto ID (+ fuzzy fallback), append new price points, flag disappeared listings via detail-page re-check.
- Two views: (a) search results (latest scan, table, price-change badges); (b) car detail (metadata + price-history chart + active/sold status).
