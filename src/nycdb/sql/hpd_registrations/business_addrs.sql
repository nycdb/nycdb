DROP TABLE IF EXISTS hpd_business_addresses;

CREATE TABLE  hpd_business_addresses AS (
     SELECT businesshousenumber,
            businessstreetname,
            businesszip,
            businessapartment,
            count(*) as numberOfContacts,
            anyarray_remove_null(array_agg(corporationname)) as corporationnames,
            anyarray_remove_null(array_agg(concat(firstname, ' ', lastname))) as ownernames,
            array_agg(registrationid) as regids,
            anyarray_uniq(array_agg(registrationid)) as uniqregids
      FROM hpd_contacts
      -- This will ensure that these three fields all contain something and arent null or empty
      WHERE (
          (businesshousenumber <> '') IS TRUE AND
          (businessstreetname <> '') IS TRUE AND
          (businesszip <> '') IS TRUE
        )
      GROUP BY businesshousenumber, businessstreetname, businesszip, businessapartment
    );

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
