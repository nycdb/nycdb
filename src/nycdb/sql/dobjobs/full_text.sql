-- owner businessname
ALTER TABLE dobjobs ADD COLUMN ownersbusinessname_tsvector tsvector;
UPDATE dobjobs SET ownersbusinessname_tsvector = to_tsvector('english', ownersbusinessname);
CREATE INDEX ownersbusinessname_tsvector_idx ON dobjobs USING GIN (ownersbusinessname_tsvector);

-- owner name
ALTER TABLE dobjobs ADD COLUMN ownername_tsvector tsvector;
UPDATE dobjobs SET ownername_tsvector = to_tsvector('english', ownername);
CREATE INDEX ownername_tsvector_idx ON dobjobs USING GIN (ownername_tsvector);

--job description
ALTER TABLE dobjobs ADD COLUMN jobdescription_tsvector tsvector;
UPDATE dobjobs SET jobdescription_tsvector = to_tsvector('english', JobDescription);
CREATE INDEX jobdescription_tsvector_idx ON dobjobs USING GIN (jobdescription_tsvector);

--applicant name
ALTER TABLE dobjobs ADD COLUMN applicantname_tsvector tsvector;
UPDATE dobjobs SET applicantname_tsvector = to_tsvector('english', applicantname);
CREATE INDEX applicantname_tsvector_idx ON dobjobs USING GIN (applicantname_tsvector);
