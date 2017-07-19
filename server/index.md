# NYC-DB API

## ABOUT

NYC-DB is a database of New York City housing data, built by and for community activists. The [code](https://github.com/aepyornis/nyc-db) behind it is free software.

## Using the API

This api is a free resource. No authorization is required and there are currently no limits. However, this api is not intended to be used to gather bulk data. Regular database dumps and instructions for how to create your own version of the database is available on the [github page](https://github.com/aepyornis/nyc-db).

The API runs off [POSTGREST](https://postgrest.com). For detailed information on how api calls work, use the [postgrest documentation](https://postgrest.com/en/v0.4/api.html) as a reference.

## End Points

The api is available here ``` https://api.nycdb.info/ ``` and is only available through TLS (HTTPS). HTTP requests will be redirected.

Each table resource is at /table_name. For instance, ``` GET /dobjobs ``` will retrive rows from the 'dobjobs' table. There is a 5,000 row limit on requests.

### Tables:

*pluto*
  - pluto_16v2
 
*dob*
  - dobjobs
 
*hpd violations*
  - hpd_violations
  - hpd_uniq_violations
  - hpd_open_violations
  - hpd_all_violations

*hpd registrations*
  - hpd_contacts
  - hpd_corporate_owners
  - hpd_registrations
  - hpd_registrations_grouped_by_bbl

*dof*
  - dof_sales

*tax bills*
  - rentstab

*311*
  - complaints_311
 
*ACRIS*
  - personal_property_legals
  - personal_property_master
  - personal_property_parties
  - real_property_legals
  - real_property_master
  - real_property_parties


## Examples

### HPD VIOLATIONS

To get all violations for a given bbl:

```
curl https://api.nycdb.info/hpd_all_violations?bbl=eq.3033320008
```

### DOB JOBS


The 20 most recent new buildings jobs in Bushwick:

```
curl -H 'Range-Unit: items' -H 'Range: 0-19' "https://api.nycdb.info/dobjobs?communityboard=eq.304&jobtype=eq.NB&order=latestactiondate.desc"
```

### HPD Registrations

Get the registration id of a building:

```
curl -G "https://api.nycdb.info/hpd_registrations" --data-urlencode "bbl=eq.<YOUR BBL>" --data-urlencode "select=registrationid"
```

Use the registration id to get the building's contacts:

```
curl -G "https://api.nycdb.info/hpd_contacts" --data-urlencode "registrationid=eq.<REGID>"
```

Use the registration id to get a list of coprorate owners:

```
curl --data "regid=<REGID>" "https://api.nycdb.info/rpc/get_corporate_owner_info_for_regid"
```
