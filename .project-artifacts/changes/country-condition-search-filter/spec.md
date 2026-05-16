# Spec — Country of origin and condition search filter fields

## Acceptance Criteria

1. **Form fields.** The New Search and Edit Search forms include two new select fields:
   - **Country of origin:** options `Any` (value `""`), `Poland` (value `"PL"`), `Germany` (`"DE"`), `France` (`"FR"`), `Italy` (`"IT"`), `United Kingdom` (`"GB"`), `United States` (`"US"`).
   - **Condition:** options `Any` (value `""`), `Not damaged` (value `"nie-uszkodzony"`), `Damaged` (value `"uszkodzony"`).

2. **Persistence.** Create and Update routes accept `country_of_origin` and `condition` form fields, store them on the `SavedSearch` row. Empty string (`""`) is accepted (means "no filter applied").

3. **Edit pre-population.** The Edit form pre-selects the saved `country_of_origin` and `condition` values.

4. **URL filter application.** When `country_of_origin` is non-empty, `_build_search_url` adds `search[filter_enum_country_origin][0]=<value>` to the Otomoto search URL. When `condition == "nie-uszkodzony"`, adds `search[filter_enum_no_accident][0]=1`. These params are omitted when the value is empty (no filter).

5. **Results page summary.** The filter summary line on `searches/results.html` (make/model/years) also shows the active country and condition values when they are non-empty.

## Out of scope

Adding other Otomoto filter params; verifying param correctness against live Otomoto (the app will try; 0-result scans tell the user the filter is too narrow); migrating existing rows (existing defaults of `"PL"` / `"nie-uszkodzony"` are preserved).

## Key decisions

- **Empty string = no filter.** The select offers "Any" as the first option (value `""`). This is simpler than `None` and avoids nullable-column changes.
- **`search[filter_enum_no_accident][0]=1`** is the best-known Otomoto URL param for undamaged cars (based on Otomoto URL patterns). If it returns 0 results for a given search, the user can switch condition to "Any" and re-scan.
- **No new Alembic migration.** Both columns already exist on `saved_search`; the model just needs to accept `""` instead of only the previous defaults.
