# nyc-db

A database chock-full of NYC housing data.

### Datasets

- pluto: 2003 - present
- DOB JOBS
- HPD Violations
- HPD Registrations
- DOF sales
- Tax Bills - rent stabilization data

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
 - sales

*tax bills*
 - rentstab

### How it's built

The scripts to insert the data for these datasets are scatted across different repos, each using varying languages and strategies. Some of them, such as [pluto](https://github.com/aepyornis/pluto) and [HPD Violations](https://github.com/aepyornis/hpd-violations), do only one thing: insert the data into postgres. Other projects, such as [DOB-Jobs](https://github.com/aepyornis/DOB-Jobs), have their own website utilizing that data.

[PLUTO](https://github.com/aepyornis/pluto)

[Department of Building's Job Filings](https://github.com/aepyornis/DOB-Jobs)

[HPD Violations](https://github.com/aepyornis/hpd-violations)

[HPD Registrations](https://github.com/aepyornis/hpd)

[DOF Sales](https://github.com/aepyornis/dof-sales)

[Rent Stabilization Unit Counts](https://github.com/aepyornis/nyc-stabilization-unit-counts-to-pg)

### Datasets to add:
    - ACRIS
    - hpd complaints
    - selected 311 complaints
