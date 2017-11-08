# nyc-db

Let's research the landlord! New York City is in a housing crisis. Some [landlords](https://youtu.be/o1SzKHXz8tU) leave their buildings in despair and let their tenants suffer without heat in winter. Others evict their tenants, legally or illegally, in order to flip buildings and profit off of gentrification. Affordable housing is a scarce resource. 

Residents, lawyers, tenants, and organizers who want to use data in their struggle turn to proprietary databases and resources, like PropertyShark, designed for real estate or contend with CSV and printouts from city websites. NYC-DB aims to give technologists and researchers who want to volunteer their time helping community groups who are defending the city against the real estate industry a leg up by providing a ready-to-use database filled with housing data.

NYC-DB builds a postgresql database containing the following datasets:

- Department of City Planning's Pluto
- DOB Job Filings
- DOB Complaints
- HPD Violations
- HPD Registrations
- HPD Complaints
- Department of Finance Rolling Sales
- Tax bills - Rent Stabilization Unit Counts (John Krauss's data)
- 311 Complaints
- ACRIS

## Get a copy

Just want a copy of the database?

Here are the latest versions available to download from S3:

- [nyc-db-2017-11-08.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2017-11-08.sql.bz2)
- [nyc-db-2017-10-13.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2017-10-13.sql.bz2)
- [nyc-db-2017-09-08.sql.bz2](https://s3.amazonaws.com/nyc-db/nyc-db-2017-09-08.sql.bz2)

It's ~1.8gb compressed and ~16gb decompressed.

If you have aws cli installed, you can download it easily this way: ``` aws s3 cp s3://nyc-db/nyc-db-2017-11-08.sql.bz2 ./ ```

To decompress: ```  bunzip2 nyc-db-2017-11-08.sql.bz2 ```

Load the db: ``` psql -d database-name -f nyc-db-2017-11-08.sql ```

## Build it yourself!

**Upgrade in progress**: Work is being done to convert the set of scripts and Makefiles into a single python program. See the ``` src ``` folder for more information.

###  Installation

*Requirements*

Postgres and slew of common tools including python, python3, ruby, make, git, and wget. I recommend using Ansible or Docker if you can. See the ``` Dockerfile ``` for a list of required packages for Debian or Ubuntu.

*Setup*

Clone the repo: ``` git clone https://github.com/aepyornis/nyc-db.git --recursive ```

Create a pg database if you don't have one setup already: ``` createdb nycdb```

### Run

These must be run from the root of the repo. Expect this whole process to take a few hours.

Download the data files: ``` make download ```

Build the database: ``` make nyc-db ```

There are 4 connection variables that you can pass to configure the postgres connection. For instance:

```
make nyc-db DB_HOST=localhost DB_DATABASE=nycdb DB_USER=databaseuser DB_PASSWORD=mypassword
```

#### Run options: _Individual datasets_

If you want only one dataset or if you prefer to import the datasets one-at-a-time, you can run the download script (if required) with the name of the dataset and then execute the script for the corresponding dataset.

For example, to import only DOF sales data do: ``` ./download.sh dofsales ``` and ``` make dofsales ```

Notes: 
 - The scripts will drop existing tables of the same name from the database and re-populate them. This means you can re-run the scripts when new data is released.
 - Some indexes are created, but you might find yourself needing additional indexes.

Some of the scripts are stored in separate repos and are kept as submodules in the _modules_ folder:

- [PLUTO](https://github.com/aepyornis/pluto)
- [Department of Building's Job Filings](https://github.com/aepyornis/dob-jobs-parser)
- [HPD Violations](https://github.com/aepyornis/hpd-violations)
- [HPD Registrations](https://github.com/aepyornis/hpd)
- [DOF Sales](https://github.com/aepyornis/dof-sales)


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

### TABLES

*pluto*
  - pluto_16v2
 
*dob*
  - dobjobs
  - dob_complaints

*hpd* 
  - hpd_violations
  - hpd_uniq_violations
  - hpd_open_violations
  - hpd_all_violations
  - hpd_contacts
  - hpd_corporate_owners
  - hpd_registrations
  - hpd_registrations_grouped_by_bbl
  - hpd_complaints

*dof*
  - dof_sales

*tax bills*
  - rentstab

*311*
  - complaints_311
 
*ACRIS*
  - country_codes
  - document_control_codes
  - ucc_collateral_codes
  - personal_property_legals
  - personal_property_master
  - personal_property_parties
  - personal_property_references
  - personal_property_remarks
  - real_property_legals
  - real_property_master
  - real_property_parties
  - real_property_references
  - real_property_remarks

### Acknowledgments

- [@fitner](https://github.com/fitnr) for their brilliant [acris downloader](https://github.com/fitnr/acris-download)
- [@jordanderson](https://github.com/jordanderson) for a [very useful ruby library for geocoding NYC addresses](https://github.com/jordanderson/nyc_geosupport).
- [Heatseek](https://heatseek.org/) for ongoing support of the project and for their amazing work.
- [@talos](https://github.com/talos) for his [tax bill scrapping](https://github.com/talos/nyc-stabilization-unit-counts) to get counts of rent-stabilization units

### Future datasets to add:

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
