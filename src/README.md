# NYCDB

**a tool for building a database of NYC housing data**

This is a Python library and cli tool for installing, updating and managing NYCDB, a postgres database of NYC Housing Data.

For more background information on this project, the api, and to download the full database dump see: https://github.com/nycdb/nycdb


## Requirements and Installation


* python 3.6+
* Postgres 12

The latest version can be installed from pypi with pip:  ` pip3 install nycdb `


## Using NYCDB


`nycdb` downloads datasets and imports them into postgres.

View options and usage: `nycdb --help`

To print a list of datasets: ` nycdb --list-datasets`

To load all of hpd violations:

``` sh
nycdb --download hpd_violations
nycdb --load hpd_violations -P YOUR_PG_PASSWORD -D YOUR_DATABASE
```

After a dataset has been loaded you can verify it with "--verify"

``` sh
nycdb --verify hpd_violations
nycdb --verify-all
```

By default the downloaded data files are is stored in './data'. Use `--root-dir` if you'd like to change the location of the data directory.

To see more options run:

## Development

###  Adding New Datasets

[Guide Here](ADDING_NEW_DATASETS.md)
