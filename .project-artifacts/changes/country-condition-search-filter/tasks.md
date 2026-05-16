# Tasks — Country of origin and condition search filter fields

- [x] T01 — DESIGN — `searches/form.html`: add country_of_origin and condition select fields; correct selected option on edit
- [x] T02 — DEV — `searches.py` create route: read `country_of_origin` and `condition` from Form; pass to SavedSearch
- [x] T03 — DEV — `searches.py` update route: read and persist `country_of_origin` and `condition`; pre-populate `values` dict in edit_form
- [x] T04 — DEV — `engine.py` `_build_search_url`: re-add country and condition URL params conditionally
- [x] T05 — DESIGN — `searches/results.html`: show country/condition in filter summary line when non-empty
