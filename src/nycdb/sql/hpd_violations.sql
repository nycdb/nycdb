CREATE INDEX hpd_violations_bbl_idx on hpd_violations (bbl);
CREATE UNIQUE INDEX hpd_violations_violationid_idx on hpd_violations (violationid);
CREATE INDEX hpd_violations_currentstatusid_idx on hpd_violations (currentstatusid);
CREATE INDEX hpd_violations_bin_idx on hpd_violations (bin);
