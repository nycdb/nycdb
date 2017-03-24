# nyc-db

Builds a postgres database of NYC housing data, containing the following datasets:

- Pluto
- Department of Buildings Job Filings
- HPD Violations
- HPD Registrations
- Department of Finance Rolling Sales
- Tax bills - Rent Stabilization Unit Counts (John Krauss's data)

### Installation

*Requirements*

On Debian & Ubuntu, issue this command to install the requirements: 

``` sudo apt-get install build-essential wget python python3 python3-dev python3-psycopg2 python3.4-venv postgresql-client unzip git ```

On Debian Testing  use  ``` python3-venv ``` instead of ``` python3.4-venv ```

*Setup*

Clone the repo: ``` git clone https://github.com/aepyornis/nyc-db.git --recursive ```

Create a pg database if you don't have one setup already: ``` createdb nycdb```

Rename env.sh.sample to env.sh and modify it according to how postgres is setup. _env.sh_ defines two functions -- execute_sql and execute_sql_cmd -- which simply defines two wrapper functions for 'psql', based on how your postgres connection settings. It aso stores a connection string in an env variable used by python.

Example env.sh:

``` bash
export PGPASSWORD=YOURPGPASSWORD

execute_sql () {
 psql -h 127.0.0.1 -d nycdb -U postgres -f $1
}

execute_sql_cmd () {
 psql -h 127.0.0.1 -d nycdb -U postgres --command "$1"
}

NYCDB_CONNECTION_STRING="dbname=nycdb user=postgres password=YOURPGPASSWORD host=127.0.0.1"

```

Additionally, take a look at docs/sample_setup.sh for a rough idea of how to setup up a debian or ubuntu server with the database.

### Run

These must be run from the root of the repo. Expect this whole process to take an hour.

Download the data files: ``` make download ```

Build the database: ``` make nyc-db ```

#### Run options:

By default it only includes the most recent pluto. If you you'd like to include 14 (!) versions of pluto for historic analysis run the download and db script with the flag --pluto-all: ``` ./scripts/download.sh all --pluto-all ``` and ``` ./scripts/nyc_db.sh --pluto-all ```

Or use the make commands:  ```  make download-pluto-all ``` and ``` make nyc-db-pluto-all ```

Notes: 
 - The scripts will drop existing tables of the same name from the database and re-populate them. This means you can re-run the scripts when new data is released.
 - Some but not all of the tables have indexes. 

*Individual datasets*
If you want only one dataset or if you prefer to import the datasets one-at-a-time, you can run the download script with the name of the dataset and then execute the script for the corresponding dataset.

For example, to import only DOF sales data do: ``` ./scripts/download.sh dofsales ``` and ``` ./scripts/dofsales.sh ```

The scripts to insert the data for each datasets are stored in separate repos and are kept as submodules in the _modules_ folder: 

- [PLUTO](https://github.com/aepyornis/pluto)
- [Department of Building's Job Filings](https://github.com/aepyornis/dob-jobs-parser)
- [HPD Violations](https://github.com/aepyornis/hpd-violations)
- [HPD Registrations](https://github.com/aepyornis/hpd)
- [DOF Sales](https://github.com/aepyornis/dof-sales)
- [Rent Stabilization Unit Counts](https://github.com/aepyornis/nyc-stabilization-unit-counts-to-pg)

## If you like docker:

This requires docker, docker-compose, git, wget, make, and unzip.

Clone the repo: ``` git clone https://github.com/aepyornis/nyc-db.git --recursive ```

_In root of repo:_

Setup docker:  ```  make docker-setup ```

Download the data files: ``` make download ```

Create the database: ``` make docker-run ```

_After the database is built:_

Enter a psql shell: ``` make docker-shell ```

Make database dump: ``` make docker-dump ```

Run the database standalone: ``` make docker-db-standalone ``` 

## If you like ansible:

Create a fresh debian jessie or ubuntu 16 server and configure your ansible hosts file. It might end up looking something like this:

``` 
xx.xx.xx.xx ansible_user=root ansible_ssh_private_key_file=/path/to/ssh/key
```

then run the playbook: ``` cd ansible && ansible-playbook playbook.yml ```

After it's done. SSH into the server and run:

```
cd /srv/nyc-db
make download
make nyc-db
```

### TABLES

*pluto*
 - pluto_03c
 - pluto_04c
 - pluto_05d
 - pluto_06c
 - pluto_07c
 - pluto_09v2
 - pluto_10v2
 - pluto_11v2
 - pluto_12v2
 - pluto_13v2
 - pluto_14v2
 - pluto_15v1
 - pluto_16v1
 - pluto_16v2
 
*dob*
 - dobjobs
 
*hpd violations*
 - violations
 - uniq_violations
 - open_violations
 - all_violations

*hpd registrations*
 - hpd.contacts
 - hpd.corporate_owners
 - hpd.registrations
 - hpd.registrations_grouped_by_bbl

*dof*
 - dof_sales

*tax bills*
 - rentstab


### Future datasets to add:

- ACRIS
- hpd complaints
- selected 311 complaints
- census data

#### LICENSE: GPLv3

```
NYC-DB - Postgres database of NYC housing data
Copyright (C) 2016  Ziggy Mintz

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
