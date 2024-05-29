ALTER TABLE oca_index ADD PRIMARY KEY (indexnumberid);

CREATE INDEX ON oca_causes (indexnumberid);

CREATE INDEX ON oca_addresses (indexnumberid);

CREATE INDEX ON oca_parties (indexnumberid);

CREATE INDEX ON oca_events (indexnumberid);

-- "appearanceid" is not in the original data, but created in 
-- process of parsing the XML to allow for splitting out the 
-- appearance outcomes into a separate table that can still be 
-- linked back to the main appearance records that they were 
-- originally nested under in the XML.

ALTER TABLE oca_appearances ADD PRIMARY KEY (indexnumberid, appearanceid);
CREATE INDEX ON oca_appearances (indexnumberid);
CREATE INDEX ON oca_appearances (appearanceid);

CREATE INDEX ON oca_appearance_outcomes (indexnumberid, appearanceid);
CREATE INDEX ON oca_appearance_outcomes (indexnumberid);
CREATE INDEX ON oca_appearance_outcomes (appearanceid);

-- (indexnumberid, sequence) should be unique, but not
CREATE INDEX ON oca_motions (indexnumberid, sequence);
CREATE INDEX ON oca_motions (indexnumberid);
CREATE INDEX ON oca_motions (sequence);

ALTER TABLE oca_decisions ADD PRIMARY KEY (indexnumberid, sequence);
CREATE INDEX ON oca_decisions (indexnumberid);
CREATE INDEX ON oca_decisions (sequence);

ALTER TABLE oca_judgments ADD PRIMARY KEY (indexnumberid, sequence);
CREATE INDEX ON oca_judgments (indexnumberid);
CREATE INDEX ON oca_judgments (sequence);

-- In the original XML data warrants are nested under judgments, so to 
-- split out the separate warrants table the "sequence" from the 
-- judgement is added as the "judgmentsequence" column in the warrants 
-- table so they can be linked back.
ALTER TABLE oca_warrants ADD PRIMARY KEY (indexnumberid, judgmentsequence, sequence);
CREATE INDEX ON oca_warrants (indexnumberid);
CREATE INDEX ON oca_warrants (judgmentsequence);
CREATE INDEX ON oca_warrants (sequence);


ALTER TABLE oca_metadata ADD PRIMARY KEY (indexnumberid);
CREATE INDEX ON oca_metadata (initialdate);
