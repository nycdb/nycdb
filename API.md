# HTTP API for NYCDB

[Postgrest](https://postgrest.com) can be used to run an api for nycdb.

Here's an example postgrest configuration conf:

``` conf
db-uri       = "postgres://postgres:nycdb@127.0.0.1:5432/postgres"
db-schema    = "public"
db-anon-role = "anon"
db-pool = 10
server-port = 8080
max-rows = 5000
```

You will be to create an new postgres user named "anon":

``` sql
create role anon;
grant usage on schema public to anon;
grant select on all tables in schema public to anon;
grant execute on all functions in schema public to anon;
```
