-- In the raw data there are sometimes multiple rows for a single zip code, so
-- we need to union those together into a single multipolygon record. Since
-- nycdb keeps track of tables based on the names in the yml schema we need to
-- keep the same name.

CREATE INDEX zipcodes_geom_idx ON zipcodes USING GIST (geom);
CREATE TABLE zipcodes_temp AS (
    SELECT
        zipcode,
        st_union(geom) AS geom
    FROM zipcodes
    GROUP BY zipcode
);
DROP TABLE zipcodes;
ALTER TABLE zipcodes_temp RENAME TO zipcodes;
CREATE INDEX zipcodes_geom_idx ON zipcodes USING GIST (geom);
CREATE INDEX zipcodes_zipcode_idx ON zipcodes (zipcode);
