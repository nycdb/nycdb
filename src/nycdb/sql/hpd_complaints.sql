CREATE INDEX hpd_complaints_buildingid_idx on hpd_complaints (buildingid);
CREATE INDEX hpd_complaints_complaintid_idx on hpd_complaints (complaintid);
CREATE INDEX hpd_complaint_problems_complaintid_idx on hpd_complaint_problems (complaintid);
