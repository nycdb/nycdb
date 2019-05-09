create index on hpd_corporate_owners(numberofcontacts desc);
create index on hpd_contacts(type);
create index on hpd_contacts(registrationid);
create index on hpd_contacts(registrationid) WHERE type = 'CorporateOwner';
create index on hpd_registrations(registrationid);
create index on hpd_registrations(buildingid);
