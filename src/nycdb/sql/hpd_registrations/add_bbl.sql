ALTER TABLE hpd_registrations ADD COLUMN bbl char(10);
UPDATE hpd_registrations SET bbl = cast(boroid as text) || lpad(cast(block as text), 5, '0') || lpad(cast(lot as text), 4, '0');
