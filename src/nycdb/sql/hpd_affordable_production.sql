CREATE INDEX hpd_affordable_building_bbl_idx on hpd_affordable_building (bbl);
CREATE INDEX hpd_affordable_building_project_id_idx on hpd_affordable_building (ProjectId);
CREATE INDEX hpd_affordable_building_project_name_idx on hpd_affordable_building (ProjectName);
CREATE INDEX hpd_affordable_building_building_id_idx on hpd_affordable_building (BuildingId);

CREATE INDEX hpd_affordable_project_id_idx on hpd_affordable_project (ProjectId);
CREATE INDEX hpd_affordable_project_name_idx on hpd_affordable_project (ProjectName);