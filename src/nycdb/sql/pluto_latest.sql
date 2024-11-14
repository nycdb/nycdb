-- We adjust the names from Open Data to match the direct DCP downloads we have used historically
ALTER TABLE pluto_latest RENAME COLUMN communityboard TO cd;
ALTER TABLE pluto_latest RENAME COLUMN censustract2010 TO ct2010;
ALTER TABLE pluto_latest RENAME COLUMN councildistrict TO council;
ALTER TABLE pluto_latest RENAME COLUMN postcode TO zipcode;
ALTER TABLE pluto_latest ADD COLUMN landusedesc text;
UPDATE pluto_latest SET landusedesc = CASE
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
ALTER TABLE pluto_latest ADD COLUMN latitudelongitudegeom geometry;
UPDATE pluto_latest SET latitudelongitudegeom = ST_Point(longitude, latitude, 4326);
CREATE INDEX pluto_latest_bbl_idx on pluto_latest (bbl);
CREATE INDEX pluto_latest_ownername_idx on pluto_latest (ownername);
CREATE INDEX pluto_latest_latitutde_longitude_idx on pluto_latest (latitude, longitude);
CREATE INDEX pluto_latest_latitutde_longitude_st_point_gist_idx ON pluto_latest USING GIST (latitudelongitudegeom);
