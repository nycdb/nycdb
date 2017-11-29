DROP TABLE IF EXISTS hpd_registrations_grouped_by_bbl_with_contacts;

CREATE TABLE hpd_registrations_grouped_by_bbl_with_contacts
as SELECT
  registrations.housenumber,
  registrations.streetname,
  registrations.zip,
  registrations.boro,
  registrations.registrationid,
  registrations.bbl,
  contacts.corpnames,
  contacts.ownernames
FROM hpd_registrations_grouped_by_bbl AS registrations
LEFT JOIN (
  SELECT
    -- collect the various corporation names
    anyarray_uniq(anyarray_remove_null(array_agg(corporationname))) as corpnames,

    -- craziness! json in postgres!
    -- this will filter out the (typically blank) CorporateOwner human names and any other blanks
    -- using json makes this nice to get from a query but also allows us to store key/value pairs
    -- which both the title and owner's concatenated first and last name. 
    json_agg(json_build_object('title', "type", 'value', (firstname || ' ' || lastname)))
      FILTER (
        WHERE "type" != 'CorporateOwner' AND
        firstname IS NOT NULL AND
        lastname IS NOT NULL
      )
      AS ownernames,
    registrationid
  FROM hpd_contacts
  GROUP BY registrationid
) contacts ON (registrations.registrationid = contacts.registrationid);

create index on hpd_registrations_grouped_by_bbl_with_contacts (registrationid);
