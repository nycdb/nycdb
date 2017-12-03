UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' AVE$|-AVE$| -AVE$', ' AVENUE') WHERE streetname ~ '.*(AVE$|-AVE$| -AVE$)';


-- unsure what to do about the conflict with streets?
--UPDATE registrations SET streetname = regexp_replace( streetname, '^ST.? ', 'SAINT ', 'g') WHERE streetname ~  '^ST.? .*';

-- remove periods

UPDATE hpd_registrations SET streetname = regexp_replace( streetname, '\.', '', 'g');

-- remove TH ST RD ND

UPDATE hpd_registrations SET streetname = array_to_string(regexp_matches(streetname, '(.*)(\d+)(?:TH|RD|ND|ST)( .+)'), '') WHERE streetname ~ '.*(\d+)(?:TH|RD|ND|ST)( .+).*';

-- LANE, STREET, ROAD, PARKWAY, BOULEVARD, PLACE, BEACH

UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' LA$', ' LANE', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' LN$', ' LANE', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' PL$', ' PLACE', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' ST$| STR$', ' STREET', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' RD$', ' ROAD', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' PKWY$', 'PARKWAY', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' PKWY ', ' PARKWAY ', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' BLVD$', ' BOULEVARD', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, ' BLVD ', ' BOULEVARD ', 'g');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, '^BCH ', 'BEACH ', 'g');

-- DIRECTIONS
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, '^E ', 'EAST ');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, '^W ', 'WEST ');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, '^N ', 'NORTH ');
UPDATE hpd_registrations SET streetname = regexp_replace( streetname, '^S ', 'SOUTH '); 

--UPDATE registrations SET BusinessApartment = regexp_replace( BusinessApartment, '_|\.', '', 'g');

--UPDATE registrations SET BusinessHouseNumber = regexp_replace( BusinessHouseNumber, '-| ', '', 'g');
