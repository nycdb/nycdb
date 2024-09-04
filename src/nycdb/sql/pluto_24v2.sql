-- following precedent in pluto_23v1
ALTER TABLE pluto_24v2 ADD COLUMN landusedesc text;
UPDATE pluto_24v2 SET landusedesc = CASE
      WHEN landuse = 1 THEN 'One & Two Family Buildings'
      WHEN landuse = 2 THEN 'Multi-Family Walk-Up Buildings'
      WHEN landuse = 3 THEN 'Multi-Family Elevator Buildings'
      WHEN landuse = 4 THEN 'Mixed Residential & Commercial Buildings'
      WHEN landuse = 5 THEN 'Commercial & Office Buildings'
      WHEN landuse = 6 THEN 'Industrial & Manufacturing'
      WHEN landuse = 7 THEN 'Transportation & Utility'
      WHEN landuse = 8 THEN 'Public Facilities & Institutions'
      WHEN landuse = 9 THEN 'Open Space & Outdoor Recreation'
      WHEN landuse = 10 THEN 'Parking Facilities'
      WHEN landuse = 11 THEN 'Vacant Land'
      WHEN landuse IS NULL THEN NULL
      ELSE '9999'
      END;
CREATE INDEX pluto_24v2_bbl_idx on pluto_24v2 (bbl);
