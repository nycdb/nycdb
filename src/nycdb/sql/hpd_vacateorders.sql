CREATE UNIQUE INDEX hpd_vacateorders_vacateordernumber_idx on hpd_vacateorders (vacateordernumber);
CREATE INDEX hpd_vacateorders_bbl_idx on hpd_vacateorders (bbl);
CREATE INDEX hpd_vacateorders_bin_idx on hpd_vacateorders (bin);
CREATE INDEX hpd_vacateorders_buildingid_idx on hpd_vacateorders (buildingid);
CREATE INDEX hpd_vacateorders_registrationid_idx on hpd_vacateorders (registrationid);
