-- State Assembly Districts
CREATE INDEX nyad_25a_geom_idx ON nyad_25a USING GIST (geom);

-- Congressional Districts
CREATE INDEX nycg_25a_geom_idx ON nycg_25a USING GIST (geom);

-- State Senate Districts
CREATE INDEX nyss_25a_geom_idx ON nyss_25a USING GIST (geom);

-- Municipal Court Districts
CREATE INDEX nymc_25a_geom_idx ON nymc_25a USING GIST (geom);

-- City Council Districts
CREATE INDEX nycc_25a_geom_idx ON nycc_25a USING GIST (geom);

-- Election Districts
CREATE INDEX nyed_25a_geom_idx ON nyed_25a USING GIST (geom);

-- Borough Boundaries
CREATE INDEX nybb_25a_geom_idx ON nybb_25a USING GIST (geom);

-- Community Districts
CREATE INDEX nycd_25a_geom_idx ON nycd_25a USING GIST (geom);

-- School Districts
CREATE INDEX nysd_25a_geom_idx ON nysd_25a USING GIST (geom);

-- Police Precincts
CREATE INDEX nypp_25a_geom_idx ON nypp_25a USING GIST (geom);

-- Health Area
CREATE INDEX nyha_25a_geom_idx ON nyha_25a USING GIST (geom);

-- Health Center
CREATE INDEX nyhc_25a_geom_idx ON nyhc_25a USING GIST (geom);

-- Fire Companies
CREATE INDEX nyfc_25a_geom_idx ON nyfc_25a USING GIST (geom);

-- Fire Battalions
CREATE INDEX nyfb_25a_geom_idx ON nyfb_25a USING GIST (geom);

-- Fire Divisions
CREATE INDEX nyfd_25a_geom_idx ON nyfd_25a USING GIST (geom);

-- Neighborhood Tabulation Areas (2010)
CREATE INDEX nynta2010_25a_geom_idx ON nynta2010_25a USING GIST (geom);
ALTER TABLE nynta2010_25a RENAME COLUMN ntacode TO nta2010;
CREATE INDEX nynta2010_25a_nta2010_idx ON nynta2010_25a (nta2010);

-- Neighborhood Tabulation Areas (2020)
CREATE INDEX nynta2020_25a_geom_idx ON nynta2020_25a USING GIST (geom);
CREATE INDEX nynta2020_25a_nta2020_idx ON nynta2020_25a (nta2020);

-- Census Tracts (2010)
CREATE INDEX nyct2010_25a_geom_idx ON nyct2010_25a USING GIST (geom);
CREATE INDEX nyct2010_25a_boroct2010_idx ON nyct2010_25a (boroct2010);
CREATE INDEX nyct2010_25a_ct2010_idx ON nyct2010_25a (ct2010);
ALTER TABLE nyct2010_25a RENAME COLUMN ntacode TO nta2010;

-- Census Tracts (2020)
CREATE INDEX nyct2020_25a_geom_idx ON nyct2020_25a USING GIST (geom);
CREATE INDEX nyct2020_25a_boroct2020_idx ON nyct2020_25a (boroct2020);
CREATE INDEX nyct2020_25a_ct2020_idx ON nyct2020_25a (ct2020);
CREATE INDEX nyct2020_25a_nta2020_idx ON nyct2020_25a (nta2020);
