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

- [nyc-db-2018-08-05.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2018-08-05.sql.bz2)
- [nyc-db-2018-06-18.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2018-06-18.sql.bz2)
- [nyc-db-2018-05-20.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2018-05-20.sql.bz2)


It's ~2.5gb compressed and ~14gb decompressed.

If you have aws cli installed, you can download it easily this way: ``` aws s3 cp s3://nyc-db/nyc-db-2018-08-05.sql.bz2 ./ ```

To decompress: ```  bunzip2 nyc-db-2018-08-05.sql.bz2 ```

Load the db: ``` psql -d database-name -f nyc-db-2018-08-05.sql ```

## Build it yourself!

###  Installation via pypi and using the nycdb cli tool

*Requirements*

Postgres and Python3. 

*Setup*

Install the nycdb package using pip: ```pip3 install nycdb ``` This will install the program ` nycdb `.

To download a dataset use: ``` nycdb --download [dataset-name] ```

To insert a dataset into postgres: ``` nycdb --load [dataset-name] -U [pg-user] -P [pg-dataset] -D [pg-database] ```

see ` src/README.rst ` for more information on the CLI program.

### Using the Makefile to build the database

As a convenience you can create the database in one go using this command:

```
make nyc-db DB_HOST=localhost DB_DATABASE=nycdb DB_USER=databaseuser DB_PASSWORD=mypassword
```

## Ansible playbook

In the ` /ansible ` folder there are two playbooks. playbook.yml setups a server ready to install the database at /srv/nycdb. api.yml runs the public api at https://api.nycdb.info

To use, create a fresh debian stretch server and configure your ansible hosts file. It might end up looking something like this:

```
[nycdb]
xx.xx.xx.xx ansible_user=root ansible_ssh_private_key_file=/path/to/ssh/key
```

Then run the playbook: ``` cd ansible && ansible-playbook playbook.yml ```

After it's done. SSH into the server and run:

``` bash
cd /srv/nyc-db
make -j 2 nyc-db DB_PASSWORD=[password from /ansible/credentials/nycdb_psql_pass]

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
