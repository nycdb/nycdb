ALTER TABLE real_property_legals ADD COLUMN bbl char(10);
UPDATE real_property_legals SET bbl = cast(borough as text) || lpad(cast(block as text), 5, '0') || lpad(cast(lot as text), 4, '0');

ALTER TABLE personal_property_legals ADD COLUMN bbl char(10);
UPDATE personal_property_legals SET bbl = cast(borough as text) || lpad(cast(block as text), 5, '0') || lpad(cast(lot as text), 4, '0');

