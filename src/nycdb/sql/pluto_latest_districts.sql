
-- Creates a table of all BBLs from PLUTO_LATEST with all political districts
-- spatially joined from BOUNDARIES files. Includes City Council, State
-- Assembly, State Senate, Congressional districts, Community Districts, 
-- Zip Codes, Borough, Census Tracts (2010 and 2020) and Neighborhood Tabulation
-- Areas (NTA) (2010 and 2020).

CREATE TEMP TABLE IF NOT EXISTS x_pluto_geom AS (
	SELECT
		p.bbl,
		p.address,
		p.zipcode,
		p.borocode AS borough,
		p.cd AS community_dist,
		p.council::TEXT AS coun_dist,
		p.bct2020 AS boroct2020,
		ct.nta2020, 
		ct.ntaname AS nta2020_name,
		ST_TRANSFORM(ST_SetSRID(ST_MakePoint(longitude, latitude),4326), 2263) AS geom
	FROM pluto_latest AS p
	LEFT JOIN nyct2020 AS ct ON bct2020 = boroct2020
);

CREATE INDEX ON x_pluto_geom using gist (geom);

DROP TABLE IF EXISTS pluto_latest_districts;
CREATE TABLE IF NOT EXISTS pluto_latest_districts AS (
	SELECT
		p.bbl,
		p.address,
		p.zipcode,
		p.borough,
		p.community_dist,
		p.coun_dist,
		p.boroct2020,
		p.nta2020, 
		p.nta2020_name,
		ad.assemdist::text AS assem_dist,
		ss.stsendist::text AS stsen_dist,
		cg.congdist::text AS cong_dist,
		p.geom
	FROM x_pluto_geom AS p
	LEFT JOIN nyad AS ad ON ST_Within(p.geom, ad.geom)
	LEFT JOIN nyss AS ss ON ST_Within(p.geom, ss.geom)
	LEFT JOIN nycg AS cg ON ST_Within(p.geom, cg.geom)
);

CREATE INDEX pluto_latest_districts_bbl_idx ON pluto_latest_districts (bbl);
CREATE INDEX pluto_latest_districts_geom_idx ON pluto_latest_districts using gist (geom);
