# i7-retro.md — Scan Execution & Persistence

- Country-of-origin and condition URL filters dropped: Otomoto's `search[filter_enum_country_origin]` and `search[filter_enum_damaged]` parameters returned 0 results in the verified URL encoding. Core make/model/year filters work correctly. Country/condition filtering deferred to a future iteration when the correct Otomoto parameter format is identified.
