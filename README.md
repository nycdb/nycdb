# nycdb

Let's research the landlord! New York City is in a housing crisis. Some [landlords](https://youtu.be/o1SzKHXz8tU) leave their buildings in despair and let their tenants suffer without heat in winter. Others evict their tenants, legally or illegally, in order to flip buildings and profit off of gentrification. Affordable housing is a scarce resource.

Residents, lawyers, tenants, and organizers who want to use data in their struggle turn to proprietary databases and resources, like PropertyShark, designed for real estate or contend with CSV and printouts from city websites. _nycdb_ aims to give technologists and researchers who want to volunteer their time helping community groups who are defending the city against the real estate industry a leg up by providing a ready-to-use database filled with housing data.

**nycdb** is a python program that downloads, processes, and loads the following public datasets into postgres:

- Department of City Planning's Pluto: versions 15v1, 16v2, 17v1, 18v1, 18v2, 19v1, 19v2, 20v8, 21v3, 22v1, and the [latest version via Open Data](https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-PLUTO-/64uk-42ks)
- DOB Job Filings
- [DOB Complaints](https://github.com/nycdb/nycdb/wiki/Dataset:-DOB-Complaints)
- [DOB Violations](https://github.com/nycdb/nycdb/wiki/Dataset:-DOB-Violations)
- [HPD Violations](https://github.com/nycdb/nycdb/wiki/Dataset:-HPD-Violations)
- [HPD Litigations](https://github.com/nycdb/nycdb/wiki/Dataset:-HPD-Litigations)
- HPD Registrations
- [HPD Complaints](https://github.com/nycdb/nycdb/wiki/Dataset:-HPD-Complaints)
- [HPD Repair and Vacate Orders](https://github.com/nycdb/nycdb/wiki/Dataset:-HPD-Vacate-Orders)
- Department of Finance Rolling Sales
- Department of Finance Annualized Sales
- [Department of Finance Property Tax Exemptions](https://github.com/nycdb/nycdb/wiki/Dataset:-DOF-Exemptions)
- Tax bills - Rent Stabilization Unit Counts (John Krauss and Atul Varma's data)
- [ACRIS](https://github.com/nycdb/nycdb/wiki/Dataset:-ACRIS)
- [Marshal Evictions](https://github.com/nycdb/nycdb/wiki/Dataset:-Marshal-Evictions) - From [DOI](https://data.cityofnewyork.us/City-Government/Evictions/6z8x-wfk4) via ANHD's [Displacement Alert Project](https://github.com/ANHD-NYC-CODE/anhd-council-backend) and [API](https://api.displacementalert.org/docs/) (built by [Jade Ahking](https://github.com/0xStarcat))
- [ECB Violations](https://github.com/nycdb/nycdb/wiki/Dataset:-ECB-Violations)
- [Oath Hearings](https://github.com/nycdb/nycdb/wiki/Dataset:-OATH-Hearings)
- Property Address Directory
- J-51 Exemptions
- [OCA Housing Court Records](https://github.com/nycdb/nycdb/wiki/Dataset:-OCA-Housing-Court-Records) (zipcode)
- [BBLs of NYC Housing Authority (NYCHA) Developments](https://github.com/nycdb/nycdb/wiki/Dataset:-NYCHA-BBLs) — From NYCHA via [JustFix's scraper tool](https://github.com/JustFixNYC/nycha-scraper)

## Using the database

### Create your own copy

Go to [src/README.md](src/README.md) for documentation on how to create your own copy of the database locally.

### Use the Housing Data Coalition's instance

The Housing Data Coalition hosts their own copy ("instance") of nycdb. If you are not a member of HDC and would like to use it, please contact housingdatacoalition@gmail.com

### Acknowledgments

- [Heatseek](https://heatseek.org/) for ongoing support of the project and for their amazing work.
- [@talos](https://github.com/talos) for his [tax bill scrapping](https://github.com/talos/nyc-stabilization-unit-counts) to get counts of rent-stabilization units
- NYCDB's [programmers](https://github.com/nycdb/nycdb/graphs/contributors)
- [Housing Data Coalition](https://www.housingdatanyc.org/) for their support and for hosting nycdb workshops

#### License: AGPLv3

```
NYCDB - Postgres database of NYC housing data
Copyright (C) 2016-2020 ziggy & contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
```

The database files provided on this page are licensed [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
