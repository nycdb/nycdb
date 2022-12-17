ALTER TABLE mci_applications RENAME COLUMN BuildingIdentificationNumber to bin;
ALTER TABLE mci_applications RENAME COLUMN WkBegDt to WkBegDate;
CREATE INDEX mci_applications_bbl_idx on mci_applications (bbl);
CREATE INDEX mci_applications_bin_idx on mci_applications (bin);
CREATE INDEX mci_applications_lat_lon_idx on mci_applications (latitude, longitude);
