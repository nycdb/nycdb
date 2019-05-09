CREATE INDEX dob_violations_bbl_idx on dob_violations (bbl);
CREATE UNIQUE INDEX dob_violations_isndobbisviol_idx on dob_violations (isndobbisviol);
CREATE INDEX dob_violations_violationtypecode on dob_violations (violationtypecode);
CREATE INDEX dob_violations_ecb_number_idx on dob_violations (ecbnumber);
CREATE INDEX dob_violations_bin_idx on dob_violations (bin);
