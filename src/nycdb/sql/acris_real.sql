ALTER TABLE acris_real_property_legals ADD COLUMN bbl char(10);
UPDATE acris_real_property_legals SET bbl = cast(borough as text) || lpad(cast(block as text), 5, '0') || lpad(cast(lot as text), 4, '0');

CREATE INDEX acris_real_property_legals_bbl_idx on acris_real_property_legals (bbl);

CREATE INDEX on acris_real_property_legals(documentid);
CREATE INDEX on acris_real_property_master(documentid);
CREATE INDEX on acris_real_property_parties(documentid);
CREATE INDEX on acris_real_property_references(documentid);
CREATE INDEX on acris_real_property_remarks(documentid);

CREATE INDEX on acris_real_property_master(doctype);
CREATE INDEX on acris_real_property_master(docamount);
CREATE INDEX on acris_real_property_master(docdate);
