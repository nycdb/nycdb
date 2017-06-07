# NYC-DB API

## ABOUT

NYC-DB is a database of New York City housing data, built by and for community activists. The [code](https://github.com/aepyornis/nyc-db) behind it is free software.

## Using the API

This api is a free resource. No authorization is required and there are currently no limits. However, this api is not intended to be used to gather bulk data. Regular database dumps and instructions for how to create your own version of the database is available on the [github page](https://github.com/aepyornis/nyc-db).

The API runs off [POSTGREST](https://postgrest.com). For detailed information on how api calls work, use the [postgrest documentation](https://postgrest.com/en/v0.4/api.html) as a reference.

## End Points

The api is available here ``` https://api.nycdb.info/ ``` and is only available through TLS (HTTPS). HTTP requests will be redirected.

Each table resource is at /table_name. For instance. ``` GET /dobjobs ``` will retrive rows from the 'dobjobs' table.

## BBL


### Tables:


*pluto_v2*




