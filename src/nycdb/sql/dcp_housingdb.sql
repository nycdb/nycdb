create index dcp_housingdb_bbl_idx on dcp_housingdb (bbl);
create index dcp_housingdb_bin_idx on dcp_housingdb (bin);
create index dcp_housingdb_jobnumber_idx on dcp_housingdb (jobnumber);
create index dcp_housingdb_jobtype_idx on dcp_housingdb (jobtype);
create index dcp_housingdb_datefiled_idx on dcp_housingdb (datefiled desc nulls last);
create index dcp_housingdb_datepermit_idx on dcp_housingdb (datepermit desc nulls last);
create index dcp_housingdb_datelstupd_idx on dcp_housingdb (datelstupd desc nulls last);
create index dcp_housingdb_datecomplt_idx on dcp_housingdb (datecomplt desc nulls last);
create index dcp_housingdb_latitude_idx on dcp_housingdb (latitude, longitude);
