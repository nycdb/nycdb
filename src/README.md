# NYCDB

**a tool for building a database of NYC housing data**

This is a Python library and cli tool for installing, updating and managing NYCDB, a postgres database of NYC Housing Data.

For more background information on this project and links to download copies of full database dump visit: https://github.com/nycdb/nycdb. We use the term **nycdb** to refer to both the python software and the running copy of the postgres database.

## Using the cli tool

You will need python 3.6+ and Postgres. The latest version can be installed from pypi with pip:  `python3 -m pip install nycdb`

If the installation is successful, you can view a summary of the tool's options by running `nycdb --help`

To print a list of datasets: ` nycdb --list-datasets`

`nycdb`'s main job is to download datasets and import them into postgres. It does not manage the database for you. You can use the flags `-U/--user`, `-D/--database`, `-P/--password`, and `-H/--host` to instruct nycdb to connect to the correct database. See `nycdb --help` for the defaults.

Example: downloading, loading, and verifying the dataset **hpd_violations**:

``` sh
nycdb --download hpd_violations
nycdb --load hpd_violations
nycdb --verify hpd_violations
```

You can also verify all datasets: ` nycdb --verify-all `

By default the downloaded data files are is stored in `./data`. Use `--root-dir` to change the location of the data directory.

You can export a `.sql` file for any dataset by using the `--dump` command

## Development

There are two development workflows: one using python virtual environments and one using docker.

### Using docker and docker-compose

To get started all you have to do is run `docker-compose up`.

On the first run Docker will take longer to downloads and build the images. It
will start a Postgres server on port 5432 of your local machineYou can also press
<kbd>CTRL</kbd>-<kbd>C</kbd> at any point to stop the server.

In a separate terminal, you will be able to now use the nycdb cli: `docker-compose run nycdb --help`

You can also open a python3 shell: `docker-compose run --entrypoint=python3 nycdb` or run the test suit `docker-compose run --entrypoint=pytest nycdb`

You may also develop on nycdb itself:

* Any changes you make to the tool's source code will automatically be reflected
  in future invocations of `nycdb` and the test suite.
* The postgres database server is forwarded to localhost:5432 which you can connect to via a desktop client if you like.
* If you don't have a desktop Postgres client, you can always run
  `nycdb --dbshell` to interactively inspect the database with [psql](http://postgresguide.com/utilities/psql.html).

To stop the database run `docker-compose down`. The downloaded files and database data are stored in docker volumes and are not automatically removed.

however, if you ever want to wipe the database, run `docker-compose down -v`.

### Python3 virtual environments

If you have postgres installed separately, you can use this alternative method without docker:

Setup and active a virtual environment:

``` sh
python3 -m venv venv
source venv/bin/activate
```

Install nycdb: ` pip install -e ./src`

As long as the virtual environment is activated, you can use `nycdb` directly in your shell.

###  Adding New Datasets

See the [guide here](ADDING_NEW_DATASETS.md) for the steps to add a new dataset
