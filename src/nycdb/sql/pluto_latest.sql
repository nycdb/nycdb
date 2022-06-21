-- We adjust the names from Open Data to match the direct DCP downloads we have used historically
ALTER TABLE pluto_latest RENAME COLUMN communityboard TO cd;
ALTER TABLE pluto_latest RENAME COLUMN censustract2010 TO ct2010;
ALTER TABLE pluto_latest RENAME COLUMN councildistrict TO council;
ALTER TABLE pluto_latest RENAME COLUMN postcode TO zipcode;

CREATE INDEX pluto_latest_bbl_idx on pluto_latest (bbl);
