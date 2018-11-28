CREATE INDEX ecb_violations_bbl_idx on ecb_violations (bbl);
CREATE INDEX ecb_violation_type_idx on ecb_violations (ViolationType);
CREATE INDEX ecb_violations_dob_violation_number_idx on ecb_violations (DobViolationNumber);
CREATE UNIQUE INDEX ecb_violations_isndobbisviol_idx on ecb_violations (EcbViolationNumber);
