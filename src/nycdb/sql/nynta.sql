CREATE INDEX nynta2010_geom_idx ON nynta2010 USING GIST (geom);
ALTER TABLE nynta2010 RENAME COLUMN ntacode TO nta2010;
CREATE INDEX nynta2010_nta2010_idx ON nynta2010 (nta2010);

CREATE INDEX nynta2020_geom_idx ON nynta2020 USING GIST (geom);
CREATE INDEX nynta2020_nta2020_idx ON nynta2020 (nta2020);
