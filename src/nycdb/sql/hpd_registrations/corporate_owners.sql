DROP TABLE IF EXISTS hpd_corporate_owners;

CREATE TABLE  hpd_corporate_owners AS (
       SELECT BusinessHouseNumber,
              BusinessStreetName,
              BusinessZip,
              BusinessApartment,
              count (*) as numberOfContacts,
              anyarray_remove_null(array_agg(CorporationName)) as corporationnames,
              array_agg(registrationID) as regids,
              anyarray_uniq(array_agg(registrationID)) as uniqregids
       FROM hpd_contacts
       WHERE
                (BusinessHouseNumber IS NOT NULL AND BusinessStreetName IS NOT NULL AND BusinessZip IS NOT NULL)
                AND ("type" = 'CorporateOwner')
                GROUP BY BusinessHouseNumber, BusinessStreetName, BusinessZip, BusinessApartment);

ALTER TABLE hpd_corporate_owners ADD COLUMN id serial;
UPDATE hpd_corporate_owners SET id = DEFAULT;

ALTER TABLE hpd_corporate_owners ADD PRIMARY KEY (id);
ALTER TABLE hpd_corporate_owners ADD COLUMN uniqnames text[];

UPDATE hpd_corporate_owners SET uniqnames = corporationnames;

UPDATE hpd_corporate_owners SET uniqregids = anyarray_uniq(regids);
-- there appears to be at least row that causes an error with anyarray_unique, which is 'fixed' by the WHERE clause here.
UPDATE hpd_corporate_owners SET uniqnames = anyarray_uniq(corporationnames) WHERE array_length(corporationnames, 1) > 0;
