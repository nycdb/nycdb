DROP TABLE IF EXISTS hpd_registrations_grouped_by_bbl;

CREATE TABLE hpd_registrations_grouped_by_bbl
as SELECT
   first(housenumber) as housenumber,
   first(streetname) as streetname,
   first(zip) as zip,
   first( boro) as boro,
   registrationid,
   bbl
FROM hpd_registrations
GROUP BY bbl, registrationid;

create index on hpd_registrations_grouped_by_bbl (registrationid);
