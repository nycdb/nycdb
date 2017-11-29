DROP TABLE IF EXISTS hpd_business_addresses;

CREATE TABLE  hpd_business_addresses AS (
       SELECT BusinessHouseNumber,
              BusinessStreetName,
              BusinessZip,
              BusinessApartment,
              count (*) as numberOfContacts,
              anyarray_remove_null(array_agg(CorporationName)) as corporationnames,
              anyarray_remove_null(array_agg(concat(firstname, ' ', lastname))) as ownernames,
              array_agg(registrationID) as regids,
              anyarray_uniq(array_agg(registrationID)) as uniqregids
       FROM hpd_contacts
       WHERE
                (BusinessHouseNumber IS NOT NULL AND BusinessStreetName IS NOT NULL AND  BusinessZip IS NOT NULL)
                GROUP BY BusinessHouseNumber, BusinessStreetName, BusinessZip, BusinessApartment);

ALTER TABLE hpd_business_addresses ADD COLUMN id serial;
UPDATE hpd_business_addresses SET id = DEFAULT;

ALTER TABLE hpd_business_addresses ADD PRIMARY KEY (id);
ALTER TABLE hpd_business_addresses ADD COLUMN uniqcorpnames text[];
ALTER TABLE hpd_business_addresses ADD COLUMN uniqownernames text[];

-- remove blank fields from owner columns
UPDATE hpd_business_addresses SET ownernames = array_remove(ownernames, ' ');

UPDATE hpd_business_addresses SET uniqcorpnames = corporationnames;
UPDATE hpd_business_addresses SET uniqownernames = ownernames;

UPDATE hpd_business_addresses SET uniqregids = anyarray_uniq(regids);
-- there appears to be at least row that causes an error with anyarray_unique, which is 'fixed' by the WHERE clause here.
UPDATE hpd_business_addresses SET uniqcorpnames = anyarray_uniq(corporationnames) WHERE array_length(corporationnames, 1) > 0;
UPDATE hpd_business_addresses SET uniqownernames = anyarray_uniq(ownernames) WHERE array_length(ownernames, 1) > 0;
