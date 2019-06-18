# nyc-db

Let's research the landlord! New York City is in a housing crisis. Some [landlords](https://youtu.be/o1SzKHXz8tU) leave their buildings in despair and let their tenants suffer without heat in winter. Others evict their tenants, legally or illegally, in order to flip buildings and profit off of gentrification. Affordable housing is a scarce resource.

Residents, lawyers, tenants, and organizers who want to use data in their struggle turn to proprietary databases and resources, like PropertyShark, designed for real estate or contend with CSV and printouts from city websites. NYC-DB aims to give technologists and researchers who want to volunteer their time helping community groups who are defending the city against the real estate industry a leg up by providing a ready-to-use database filled with housing data.

NYC-DB builds a postgresql database containing the following datasets:

- Department of City Planning's Pluto: versions 15v1, 16v2, 17v1, 18v1, and 18v2
- DOB Job Filings
- DOB Complaints
- HPD Violations
- HPD Registrations
- HPD Complaints
- Department of Finance Rolling Sales
- Tax bills - Rent Stabilization Unit Counts (John Krauss's data)
- ACRIS
- 2017 Marshal Evictions
- ECB / Oath Hearings
- J-51 Exemptions

NYC-DB is a python3 command line program that downloads and loads datasets into postgres.

## Get a copy

Just want a copy of the database?

Here are the latest versions available to download:

- [nyc-db-2019-06-17.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2019-06-17.sql.bz2)
- [nyc-db-2019-05-14.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2019-05-14.sql.bz2)
- [nyc-db-2019-04-09.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2019-04-09.sql.bz2)

[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

It's ~3gb compressed and ~20gb decompressed.

Load the db: ``` bzcat nyc-db-2019-06-17.sql.bz2 | psql -d database-name ```

## Adding New Datasets

[Guide Here](src/ADDING_NEW_DATASETS.md)

## Build it yourself!

### nycdb cli

To manage and create copies of the database yourself, you can see the nycdb command line tool available on pypi: ` pip3 install nycdb `

see `src/README.md` for more information on using the command line tool.

### Using the Makefile to build the database

As a convenience you can create the database in one go using this command:

```
make nyc-db DB_HOST=localhost DB_DATABASE=nycdb DB_USER=databaseuser DB_PASSWORD=mypassword
```

### Using Docker

You can also use Docker to both use and develop nycdb. This can be useful because
you only need to install Docker--you don't need to worry about installing the proper
version of Python, Postgres, or any other tools.

To proceed, first [install Docker][] and then run:

```
docker-compose up
```

After Docker downloads and builds some things, it will start a Postgres server on port
7777 of your local machine, which you can connect to via a desktop client if you like.
You can also press <kbd>CTRL</kbd>-<kbd>C</kbd> at any point to stop the server.

In a separate terminal, you can run:

```
docker-compose run app bash
```

At this point you are inside a bash shell in a container that has everything already
set up for you. The initial working directory will be `/nycdb`, which is mapped to
the root of the project's repository. From here you can run `nycdb` to access the
command-line tool.

To develop on nycdb itself:

* You can run `pytest` to run the test suite.
* Any changes you make to the tool's source code will automatically be reflected
  in future invocations of `nycdb` and/or the test suite.
* If you don't have a desktop Postgres client, you can always run
  `nycdb --dbshell` to interactively inspect the database with [`psql`][].

You can leave the bash shell with `exit`.

If you ever want to wipe the database, run `docker-compose down -v`.

[install Docker]: https://www.docker.com/get-started
[`psql`]: http://postgresguide.com/utilities/psql.html

### Setup the database and API on a cloud server

See the folder `/ansible` for ansible playbooks to setup the database on a sever.

### Acknowledgments

- [Heatseek](https://heatseek.org/) for ongoing support of the project and for their amazing work.
- [@talos](https://github.com/talos) for his [tax bill scrapping](https://github.com/talos/nyc-stabilization-unit-counts) to get counts of rent-stabilization units

### Future datasets to add:

- census data

#### LICENSE: AGPLv3

```
NYC-DB - Postgres database of NYC housing data
Copyright (C) 2016-2018 Ziggy Mintz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

The database files provided on this page are licensed [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
