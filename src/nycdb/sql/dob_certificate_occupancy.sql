ALTER TABLE dob_certificate_occupancy RENAME COLUMN binnumber TO bin;

CREATE INDEX dob_certificate_occupancy_bbl_idx on dob_certificate_occupancy (bbl);
CREATE INDEX dob_certificate_occupancy_bin_idx on dob_certificate_occupancy (bin);
CREATE INDEX dob_certificate_occupancy_jobnumber_idx on dob_certificate_occupancy (jobnumber);
CREATE INDEX dob_certificate_occupancy_coissuedate_idx on dob_certificate_occupancy (coissuedate);


ALTER TABLE dob_foil_certificate_occupancy ADD COLUMN bbl char(10);
UPDATE dob_foil_certificate_occupancy SET bbl = substr(bin, 1, 1) || lpad(block::text, 5, '0') || lpad(lot::text, 4, '0');

CREATE INDEX dob_foil_certificate_occupancy_bbl_idx on dob_foil_certificate_occupancy (bbl);
CREATE INDEX dob_foil_certificate_occupancy_bin_idx on dob_foil_certificate_occupancy (bin);
CREATE INDEX dob_foil_certificate_occupancy_jobnumber_idx on dob_foil_certificate_occupancy (jobnumber);
CREATE INDEX dob_foil_certificate_occupancy_issuedate_idx on dob_foil_certificate_occupancy (issuedate);


ALTER TABLE dob_now_certificate_occupancy ADD COLUMN bbl char(10);
UPDATE dob_now_certificate_occupancy SET bbl = substr(bin, 1, 1) || lpad(block::text, 5, '0') || lpad(lot::text, 4, '0');

CREATE INDEX dob_now_certificate_occupancy_bbl_idx on dob_now_certificate_occupancy (bbl);
CREATE INDEX dob_now_certificate_occupancy_bin_idx on dob_now_certificate_occupancy (bin);
CREATE INDEX dob_now_certificate_occupancy_jobfilingname_idx on dob_now_certificate_occupancy (jobfilingname);
CREATE INDEX dob_now_certificate_occupancy_cofoissuancedate_idx on dob_now_certificate_occupancy (cofoissuancedate);
