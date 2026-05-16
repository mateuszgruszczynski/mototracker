# Retro — Country of origin and condition search filter fields

## What was done

- Added country_of_origin and condition select fields to the search form (new + edit)
- Create/Update routes now persist both fields
- URL builder re-adds filter params conditionally (`filter_enum_country_origin`, `filter_enum_no_accident`)
- Results page shows active country and condition in the filter summary line
- No DB migration needed — columns already existed from the original schema

## Follow-up items

- The Otomoto URL params for these filters (`search[filter_enum_country_origin][0]` and `search[filter_enum_no_accident][0]`) were removed in iteration 003 because they returned 0 results. They have been re-added with best-guess names. If a scan with a specific country/condition returns 0 results unexpectedly, the Otomoto param names may need adjusting by inspecting a live Otomoto URL with those filters applied in-browser.

No plan changes.
