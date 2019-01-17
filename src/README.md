*****
NYCDB
*****

a tool for building a database of NYC housing data
**************************************************

This is a Python library and cli tool for installing, updating and managing NYC-DB, a postgres database of Housing Data for NYC.

For more background information on this project, the api, and to download the full database dump see: https://github.com/aepyornis/nyc-db


How to use
**********

**Requirements**:  Postgres and Python3


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


After a dataset has been loaded you can verify it with "--verify"

.. code-block:: bash

   nycdb --verify hpd_violations
   nycdb --verify-all


By default the downloaded data files are stores in './data'. Use --root-dir to change the location of the data directory.

To see more options run: `nycdb --help`

## Adding New Datasets

[Guide Here](ADDING_NEW_DATASETS.md)
