ALTER TABLE real_property_legals ADD COLUMN bbl char(10);
UPDATE real_property_legals SET bbl = cast(borough as text) || lpad(cast(block as text), 5, '0') || lpad(cast(lot as text), 4, '0');

ALTER TABLE personal_property_legals ADD COLUMN bbl char(10);
UPDATE personal_property_legals SET bbl = cast(borough as text) || lpad(cast(block as text), 5, '0') || lpad(cast(lot as text), 4, '0');

CREATE INDEX real_property_legals_bbl_idx on real_property_legals (bbl);
CREATE INDEX personal_property_legals_bbl_idx on personal_property_legals (bbl);

CREATE INDEX on real_property_legals(documentid);
CREATE INDEX on real_property_master(documentid);
CREATE INDEX on real_property_parties(documentid);
CREATE INDEX on real_property_references(documentid);
CREATE INDEX on real_property_remarks(documentid);

CREATE INDEX on personal_property_legals(documentid);
CREATE INDEX on personal_property_master(documentid);
CREATE INDEX on personal_property_parties(documentid);
CREATE INDEX on personal_property_references(documentid);
CREATE INDEX on personal_property_remarks(documentid);
