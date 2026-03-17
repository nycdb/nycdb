CREATE INDEX fc_shd_building_bbl_idx on fc_shd_building (bbl);

ALTER TABLE fc_shd_subsidy RENAME COLUMN refbbl to bbl;
CREATE INDEX fc_shd_subsidy_bbl_idx on fc_shd_subsidy (bbl);
