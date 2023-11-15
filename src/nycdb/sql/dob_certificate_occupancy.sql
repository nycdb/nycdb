ALTER TABLE dob_certificate_occupancy RENAME COLUMN binnumber TO bin;

CREATE INDEX dob_certificate_occupancy_bbl_idx on dob_certificate_occupancy (bbl);
CREATE INDEX dob_certificate_occupancy_bin_idx on dob_certificate_occupancy (bin);
CREATE INDEX dob_certificate_occupancy_jobnumber_idx on dob_certificate_occupancy (jobnumber);
