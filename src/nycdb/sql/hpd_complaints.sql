CREATE INDEX hpd_complaints_and_problems_receiveddate_idx on hpd_complaints (receiveddate);
CREATE INDEX hpd_complaints_and_problems_buildingid_idx on hpd_complaints (buildingid);
CREATE INDEX hpd_complaints_and_problems_complaintid_idx on hpd_complaints (complaintid);
CREATE INDEX hpd_complaints_and_problems_problemid_idx on hpd_complaints (problemid);
CREATE INDEX hpd_complaints_and_problems_bbl_idx on hpd_complaints (bbl);
CREATE INDEX hpd_complaints_and_problems_apartment_idx on hpd_complaints (apartment);
CREATE INDEX hpd_complaints_and_problems_type_idx on hpd_complaints (type);
CREATE INDEX hpd_complaints_and_problems_majorcategory_idx on hpd_complaints (majorcategory);
CREATE INDEX hpd_complaints_and_problems_minorcategory_idx on hpd_complaints (minorcategory);


CREATE INDEX hpd_complaints_buildingid_idx on hpd_complaints (buildingid);
CREATE INDEX hpd_complaints_complaintid_idx on hpd_complaints (complaintid);
CREATE INDEX hpd_complaint_problems_complaintid_idx on hpd_complaint_problems (complaintid);
CREATE INDEX hpd_complaints_bbl_idx on hpd_complaints (bbl);