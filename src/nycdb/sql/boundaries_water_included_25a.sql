-- State Assembly Districts
CREATE INDEX nyadwi_25a_geom_idx ON nyadwi_25a USING GIST (geom);

-- Congressional Districts
CREATE INDEX nycgwi_25a_geom_idx ON nycgwi_25a USING GIST (geom);

-- State Senate Districts
CREATE INDEX nysswi_25a_geom_idx ON nysswi_25a USING GIST (geom);

-- Municipal Court Districts
CREATE INDEX nymcwi_25a_geom_idx ON nymcwi_25a USING GIST (geom);

-- City Council Districts
CREATE INDEX nyccwi_25a_geom_idx ON nyccwi_25a USING GIST (geom);

-- Election Districts
CREATE INDEX nyedwi_25a_geom_idx ON nyedwi_25a USING GIST (geom);

-- Borough Boundaries
CREATE INDEX nybbwi_25a_geom_idx ON nybbwi_25a USING GIST (geom);

-- Community Districts
CREATE INDEX nycdwi_25a_geom_idx ON nycdwi_25a USING GIST (geom);

-- Census Tracts (2010)
CREATE INDEX nyct2010wi_25a_geom_idx ON nyct2010wi_25a USING GIST (geom);
CREATE INDEX nyct2010wi_25a_boroct2010_idx ON nyct2010wi_25a (boroct2010);
CREATE INDEX nyct2010wi_25a_ct2010_idx ON nyct2010wi_25a (ct2010);
ALTER TABLE nyct2010wi_25a RENAME COLUMN ntacode TO nta2010;

-- Census Tracts (2020)
CREATE INDEX nyct2020wi_25a_geom_idx ON nyct2020wi_25a USING GIST (geom);
CREATE INDEX nyct2020wi_25a_boroct2020_idx ON nyct2020wi_25a (boroct2020);
CREATE INDEX nyct2020wi_25a_ct2020_idx ON nyct2020wi_25a (ct2020);
CREATE INDEX nyct2020wi_25a_nta2020_idx ON nyct2020wi_25a (nta2020);
