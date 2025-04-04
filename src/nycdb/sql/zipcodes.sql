CREATE INDEX zipcodes_geom_idx ON zipcodes USING GIST (geom);
CREATE INDEX zipcodes_zipcode_idx ON zipcodes (zipcode);
