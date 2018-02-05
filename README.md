# nyc-db

Let's research the landlord! New York City is in a housing crisis. Some [landlords](https://youtu.be/o1SzKHXz8tU) leave their buildings in despair and let their tenants suffer without heat in winter. Others evict their tenants, legally or illegally, in order to flip buildings and profit off of gentrification. Affordable housing is a scarce resource. 

Residents, lawyers, tenants, and organizers who want to use data in their struggle turn to proprietary databases and resources, like PropertyShark, designed for real estate or contend with CSV and printouts from city websites. NYC-DB aims to give technologists and researchers who want to volunteer their time helping community groups who are defending the city against the real estate industry a leg up by providing a ready-to-use database filled with housing data.

NYC-DB builds a postgresql database containing the following datasets:

- Department of City Planning's Pluto: versions 16v2 and 17v1
- DOB Job Filings
- DOB Complaints
- HPD Violations
- HPD Registrations
- HPD Complaints
- Department of Finance Rolling Sales
- Tax bills - Rent Stabilization Unit Counts (John Krauss's data)
- ACRIS

NYC-DB is a python3 command line program that downloads and loads datasets into postgres.

## Get a copy

Just want a copy of the database?

Here are the latest versions available to download from S3:

- [nyc-db-2018-02-04.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2018-02-04.sql.bz2)
- [nyc-db-2018-01-07.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2018-01-07.sql.bz2)
- [nyc-db-2017-12-15.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2017-12-15.sql.bz2)


It's ~2.5gb compressed and ~14gb decompressed.

If you have aws cli installed, you can download it easily this way: ``` aws s3 cp s3://nyc-db/nyc-db-2018-02-04.sql.bz2 ./ ```

To decompress: ```  bunzip2 nyc-db-2018-02-04.sql.bz2 ```

Load the db: ``` psql -d database-name -f nyc-db-2018-02-04.sql.bz2 ```

## Build it yourself!

###  Installation

*Requirements*

Postgres and Python. I recommend using Ansible or Docker if you can. See the ``` Dockerfile ``` for a list of required packages for Debian or Ubuntu. As of right now, Postgres 10 is not compatible. Please be sure to postgres 9.6 until those issues are fixed.

*Setup*

Clone the repo: ``` git clone https://github.com/aepyornis/nyc-db.git --recursive ```

Create a pg database if you don't have one setup already: ``` createdb nycdb```

### Quickly create the whole database:

These must be run from the root of the repo. Expect this whole process to take a few hours.

Download the data files: ``` make download ```

Build the database: ``` make nyc-db ```

There are 4 connection variables that you can pass to configure the postgres connection. For instance:

```
make nyc-db DB_HOST=localhost DB_DATABASE=nycdb DB_USER=databaseuser DB_PASSWORD=mypassword
```

## NYCDB CLI TOOL

The Makefile is just a convenience for running the nycdb cli program, which will enable you to  customize your installation more, such as only importing some of the datasets.  See the README.md in the  ` ./src ` directory.

## If you like docker:

Clone the repo: ``` git clone https://github.com/aepyornis/nyc-db.git ```

_In root of repo:_

Setup docker:  ```  make docker-setup ```

Download the data files: ``` make download ```

Create the database: ``` make docker-run ```

_After the database is built:_

Enter a psql shell: ``` make docker-shell ```

Make database dump: ``` make docker-dump ```

Run the database standalone: ``` make docker-db-standalone ``` 

## If you like ansible:

Create a fresh debian stretch or ubuntu 16 server and configure your ansible hosts file. It might end up looking something like this:

```
[nycdb]
xx.xx.xx.xx ansible_user=root ansible_ssh_private_key_file=/path/to/ssh/key
```

Then run the playbook: ``` cd ansible && ansible-playbook playbook.yml ```

After it's done. SSH into the server and run:

``` bash
cd /srv/nyc-db
make download
make nyc-db
```

### Acknowledgments

- [Heatseek](https://heatseek.org/) for ongoing support of the project and for their amazing work.
- [@talos](https://github.com/talos) for his [tax bill scrapping](https://github.com/talos/nyc-stabilization-unit-counts) to get counts of rent-stabilization units

### Future datasets to add:

- census data

#### LICENSE: GPLv3

```
NYC-DB - Postgres database of NYC housing data
Copyright (C) 2016-2017 Ziggy Mintz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
