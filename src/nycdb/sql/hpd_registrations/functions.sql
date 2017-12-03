DROP FUNCTION IF EXISTS get_corporate_owner_info_for_regid(int);

CREATE OR REPLACE FUNCTION get_corporate_owner_info_for_regid(regid int)
RETURNS TABLE (id int, buildingscount int, uniqnames text[], businesshousenumber text, businessstreetname text, businesszip text) AS $$
      SELECT id,
      	     array_length(anyarray_uniq(regids), 1) as buildingcount,
	     uniqnames,
	     businesshousenumber,
	     businessstreetname,
	     businesszip
      FROM hpd_corporate_owners WHERE get_corporate_owner_info_for_regid.regid = ANY(regids)
$$ LANGUAGE SQL;


-- Returns one or more Registered Business Address (and associated info) from an address
DROP FUNCTION IF EXISTS get_rbas_from_addr(text, text, text);

CREATE OR REPLACE FUNCTION get_rbas_from_addr(_housenumber text, _streetname text, _boro text)
RETURNS TABLE (
  id int,
  businesshousenumber text,
  businessstreetname text,
  businesszip text,
  businessapartment text,
  numberofcontacts bigint,
  numberofbuildings int,
  uniqregids integer[],
  uniqcorpnames text[],
  uniqownernames text[]
) AS $$
  SELECT
    id,
    businesshousenumber,
    businessstreetname,
    businesszip,
    businessapartment,
    numberofcontacts,
    array_length(uniqregids,1) AS numberofbuildings,
    uniqregids,
    uniqcorpnames,
    uniqownernames
  FROM hpd_business_addresses AS rbas
  INNER JOIN (
    -- get registrationid from address
    SELECT DISTINCT registrationid
    FROM hpd_registrations_grouped_by_bbl r
    WHERE
      r.housenumber = _housenumber AND
      r.streetname = _streetname AND
      r.boro = _boro
  ) r ON (r.registrationid = any(rbas.uniqregids))
$$ LANGUAGE SQL;


-- Returns address info from an array of regids, which are supplied as a
-- comma delineated string
DROP FUNCTION IF EXISTS get_addrs_from_regids(text);

CREATE OR REPLACE FUNCTION get_addrs_from_regids(_regids text)
RETURNS TABLE (
  housenumber text,
  streetname text,
  boro text,
  zip text,
  regid int,
  bbl char(10),
  corpnames text[],
  ownernames json
) AS $$
  SELECT
    housenumber,
    streetname,
    boro,
    zip,
    regid,
    bbl,
    corpnames,
    ownernames
  FROM hpd_registrations_grouped_by_bbl_with_contacts AS r
  INNER JOIN (
    SELECT unnest(string_to_array(_regids, ','))::int AS regid
  ) regids ON (r.registrationid = regids.regid)
$$ LANGUAGE SQL;
