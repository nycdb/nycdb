CREATE INDEX hpd_ll44_buildings_bbl_idx on hpd_ll44_buildings (bbl);
CREATE INDEX hpd_ll44_buildings_projectid_idx on hpd_ll44_buildings (projectid);
CREATE INDEX hpd_ll44_buildings_buildingid_idx on hpd_ll44_buildings (buildingid);

CREATE INDEX hpd_ll44_projects_projectid_idx on hpd_ll44_projects (projectid);

CREATE INDEX hpd_ll44_disqualified_list_bbl_idx on hpd_ll44_disqualified_list (bbl);
