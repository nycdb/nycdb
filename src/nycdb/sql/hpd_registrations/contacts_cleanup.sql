
-- Null out values consisting purely of non-alphanumeric chars (\W), X's, and/or whitespace (\s)
UPDATE hpd_contacts SET contactdescription = nullif(regexp_replace(contactdescription,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET corporationname = nullif(regexp_replace(corporationname,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET title = nullif(regexp_replace(title,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET firstname = nullif(regexp_replace(firstname,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET lastname = nullif(regexp_replace(lastname,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET businesshousenumber = nullif(regexp_replace(businesshousenumber,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET businessstreetname = nullif(regexp_replace(businessstreetname,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET businessapartment = nullif(regexp_replace(businessapartment,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET businesscity = nullif(regexp_replace(businesscity,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET businessstate = nullif(regexp_replace(businessstate,'^(\W|X|\s)*$', ''),'');
UPDATE hpd_contacts SET businesszip = nullif(regexp_replace(businesszip,'^(\W|X|\s)*$', ''),'');

-- Null out middle initials that aren't letters, @, or & (which apparently people use...)
UPDATE hpd_contacts SET middleinitial = nullif(regexp_replace(middleinitial,'^[^a-zA-Z@&]*$', ''),'');
