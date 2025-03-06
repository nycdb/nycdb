CREATE INDEX nyad_geom_idx ON nyad USING GIST (geom);
CREATE INDEX nycg_geom_idx ON nycg USING GIST (geom);
CREATE INDEX nyss_geom_idx ON nyss USING GIST (geom);
CREATE INDEX nymc_geom_idx ON nymc USING GIST (geom);
CREATE INDEX nycc_geom_idx ON nycc USING GIST (geom);
CREATE INDEX nyed_geom_idx ON nyed USING GIST (geom);
CREATE INDEX nybb_geom_idx ON nybb USING GIST (geom);
CREATE INDEX nycd_geom_idx ON nycd USING GIST (geom);
CREATE INDEX nysd_geom_idx ON nysd USING GIST (geom);
CREATE INDEX nypp_geom_idx ON nypp USING GIST (geom);
CREATE INDEX nyha_geom_idx ON nyha USING GIST (geom);
CREATE INDEX nyhc_geom_idx ON nyhc USING GIST (geom);
CREATE INDEX nyfc_geom_idx ON nyfc USING GIST (geom);
CREATE INDEX nyfb_geom_idx ON nyfb USING GIST (geom);
CREATE INDEX nyfd_geom_idx ON nyfd USING GIST (geom);

-- NTAs
CREATE INDEX nynta2010_geom_idx ON nynta2010 USING GIST (geom);
ALTER TABLE nynta2010 RENAME COLUMN ntacode TO nta2010;
CREATE INDEX nynta2010_nta2010_idx ON nynta2010 (nta2010);

CREATE INDEX nynta2020_geom_idx ON nynta2020 USING GIST (geom);
CREATE INDEX nynta2020_nta2020_idx ON nynta2020 (nta2020);

-- Census Tracts
CREATE INDEX nyct2010_geom_idx ON nyct2010 USING GIST (geom);
CREATE INDEX nyct2010_boroct2010_idx ON nyct2010 (boroct2010);
CREATE INDEX nyct2010_ct2010_idx ON nyct2010 (ct2010);
ALTER TABLE nyct2010 RENAME COLUMN ntacode TO nta2010;

CREATE INDEX nyct2020_geom_idx ON nyct2020 USING GIST (geom);
CREATE INDEX nyct2020_boroct2020_idx ON nyct2020 (boroct2020);
CREATE INDEX nyct2020_ct2020_idx ON nyct2020 (ct2020);
CREATE INDEX nyct2020_nta2020_idx ON nyct2020 (nta2020);
