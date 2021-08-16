-- Here, we're renaming new column names to match their historic names such that old SQL code doesn't break:
ALTER TABLE marshal_evictions_all RENAME COLUMN residentialcommercial TO residentialcommercialind;
ALTER TABLE marshal_evictions_all RENAME COLUMN evictionapartmentnumber TO evictionaptnum;
ALTER TABLE marshal_evictions_all RENAME COLUMN marshal1stname TO marshalfirstname;
ALTER TABLE marshal_evictions_all RENAME COLUMN evictionpostcode TO evictionzip;

CREATE INDEX marshal_evictions_18_bbl_idx on marshal_evictions_18 (bbl);
CREATE INDEX marshal_evictions_19_bbl_idx on marshal_evictions_19 (bbl);
CREATE INDEX marshal_evictions_all_bbl_idx on marshal_evictions_all (bbl);
