ALTER TABLE hpd_ll44_buildings ADD COLUMN boroid int;
UPDATE hpd_ll44_buildings SET boroid = nullif(nullif(substr(bin, 1, 1), ''), '-')::int;

CREATE INDEX hpd_ll44_buildings_bbl_idx on hpd_ll44_buildings (bbl);
CREATE INDEX hpd_ll44_buildings_projectid_idx on hpd_ll44_buildings (projectid);
CREATE INDEX hpd_ll44_buildings_buildingid_idx on hpd_ll44_buildings (buildingid);

CREATE INDEX hpd_ll44_projects_projectid_idx on hpd_ll44_projects (projectid);

CREATE INDEX hpd_ll44_tax_incentive_projectid_idx on hpd_ll44_tax_incentive (projectid);
CREATE INDEX hpd_ll44_tax_incentive_taxincentivedwid_idx on hpd_ll44_tax_incentive (taxincentivedwid);
CREATE INDEX hpd_ll44_tax_incentive_taxincentivename_idx on hpd_ll44_tax_incentive (taxincentivename);
