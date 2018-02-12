*****
NYCDB
*****

a tool for building a database of NYC housing data
**************************************************

This is a Python library and cli tool for installing, updating and managing NYC-DB, a postgres database of Housing Data for NYC.

why is this needed?
*******************

New York City is in a housing crisis. Some landlords leave their buildings in despair and let their tenants suffer without heat in winter. Others evict their tenants, legally or illegally, in order to flip buildings and profit off of gentrification. Affordable housing is a scarce resource.

Residents, lawyers, tenants, and organizers who want to use data in their struggle turn to proprietary databases and resources, like PropertyShark, designed for real estate or contend with CSV and printouts from city websites. NYC-DB aims to give technologists and researchers who want to volunteer their time helping community groups who are defending the city against the real estate industry a leg up by providing a ready-to-use database filled with housing data.

How to use
**********

After installing via pip:

.. code-block:: bash

    pip3 install nycdb


You'll be able to use the program `nycdb` to import a database.

For example to load all of hpd violations:

.. code-block:: bash

    nycdb --download hpd_violations
    nycdb --load hpd_violations -P YOUR_PG_PASSWORD -D YOUR_DATABASE

To see all possible datasets:

.. code-block:: bash

   nycdb --list-datasets


By default the downloaded data files are stores in './data'. Use --root-dir to change the location of the data directory.

To see more options run: `nycdb --help`

