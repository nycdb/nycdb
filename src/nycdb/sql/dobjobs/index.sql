-- bbl
create index on dobjobs (bbl);
-- bin
create index on dobjobs (bin);
-- Latest Action Date 
create index on dobjobs (LatestActionDate DESC NULLS LAST);
create index on dobjobs (LatestActionDate DESC);	
-- jobtype
create index on dobjobs (JobType);
-- job status
create index on dobjobs (JobStatus);
-- community board
create index on dobjobs (CommunityBoard);
-- existing/proposed # of stories
create index on dobjobs (ExistingNoofStories);
create index on dobjobs (ProposedNoofStories);

create index dob_now_jobs_bbl on dob_now_jobs (bbl);
create index dob_now_jobs_bin on dob_now_jobs (bin);
create index dob_now_jobs_jobfilingnumber on dob_now_jobs (JobFilingNumber);
create index dob_now_jobs_jobtype on dob_now_jobs (JobType);
create index dob_now_jobs_filingdate on dob_now_jobs (FilingDate DESC NULLS LAST);
create index dob_now_jobs_permitissuedate on dob_now_jobs (PermitIssueDate DESC NULLS LAST);
