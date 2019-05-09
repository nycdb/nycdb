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
