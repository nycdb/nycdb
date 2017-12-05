alter table dobjobs add column address text;
alter table dobjobs add column ownername text;
alter table dobjobs add column applicantname text;

update dobjobs
       set address = house || ' ' || streetname || ', ' || zip,
       ownername = ownersfirstname || ' ' || ownerslastname,
       applicantname = applicantsfirstname || ' ' || applicantslastname;
