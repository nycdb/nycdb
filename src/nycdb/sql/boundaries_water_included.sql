-- State Assembly Districts
CREATE INDEX nyadwi_geom_idx ON nyadwi USING GIST (geom);

-- Congressional Districts
CREATE INDEX nycgwi_geom_idx ON nycgwi USING GIST (geom);

-- State Senate Districts
CREATE INDEX nysswi_geom_idx ON nysswi USING GIST (geom);

-- Municipal Court Districts
CREATE INDEX nymcwi_geom_idx ON nymcwi USING GIST (geom);

-- City Council Districts
CREATE INDEX nyccwi_geom_idx ON nyccwi USING GIST (geom);

-- Election Districts
CREATE INDEX nyedwi_geom_idx ON nyedwi USING GIST (geom);

-- Borough Boundaries
CREATE INDEX nybbwi_geom_idx ON nybbwi USING GIST (geom);

-- Community Districts
CREATE INDEX nycdwi_geom_idx ON nycdwi USING GIST (geom);

-- Census Tracts (2010)
CREATE INDEX nyct2010wi_geom_idx ON nyct2010wi USING GIST (geom);
CREATE INDEX nyct2010wi_boroct2010_idx ON nyct2010wi (boroct2010);
CREATE INDEX nyct2010wi_ct2010_idx ON nyct2010wi (ct2010);
ALTER TABLE nyct2010wi RENAME COLUMN ntacode TO nta2010;

-- Census Tracts (2020)
CREATE INDEX nyct2020wi_geom_idx ON nyct2020wi USING GIST (geom);
CREATE INDEX nyct2020wi_boroct2020_idx ON nyct2020wi (boroct2020);
CREATE INDEX nyct2020wi_ct2020_idx ON nyct2020wi (ct2020);
CREATE INDEX nyct2020wi_nta2020_idx ON nyct2020wi (nta2020);
