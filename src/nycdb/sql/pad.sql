CREATE INDEX ON pad_adr (bin);

CREATE INDEX ON pad_adr (bbl, lhnd, stname)
WHERE NULLIF(TRIM(lhnd), '') IS NOT NULL
  AND NULLIF(TRIM(stname), '') IS NOT NULL;
