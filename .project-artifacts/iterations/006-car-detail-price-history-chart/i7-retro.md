# i7-retro.md — Car Detail & Price-History Chart

## What went well

- Chart.js integration was straightforward; the `| safe` pattern established in iteration 005 (results page) applied directly.
- `subqueryload` kept the route to a single DB round-trip.
- All 5 ACs passed in Integration on the first attempt.

## What could improve

- Detail page links from the results table (iteration 005) are already wired via Alpine.js `window.location`, so the page is reachable from the normal flow.

## Plan changes

None — backlog unchanged.
