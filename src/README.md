# NYCDB

**a tool for building a database of NYC housing data**

This is a Python library and cli tool for installing, updating and managing NYCDB, a postgres database of NYC Housing Data.

For more background information on this project and links to download copies of full database dump visit: https://github.com/nycdb/nycdb. We use the term **nycdb** to refer to both the python software and the running copy of the postgres database.

## Using the cli tool

You will need python 3.6+ and Postgres. The latest version can be installed from pypi with pip:  ` python3 -m pip install nycdb `

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

### python3 virtual environments

First check your python version to make sure you have 3.6 or higher: `python3 --version`

Setup the virtual environment and install the requirements: `make init`

Install nycdb into the virtual environment: ` make install`

Run the tests: `make test`

Run only the unit tests: `make test-unit`

### Using docker

This reuqires docker and docker-compose.

To get started run ` docker-compose up `

After Docker downloads and builds some things, it will start a Postgres server on port
7777 of your local machine, which you can connect to via a desktop client if you like.
You can also press <kbd>CTRL</kbd>-<kbd>C</kbd> at any point to stop the server.

In a separate terminal, you can run:

```
docker-compose run app bash
```

At this point you are inside a bash shell in a container that has everything already
set up for you. The initial working directory will be `/nycdb`, which is mapped to
the root of the project's repository. From here you can run `nycdb` to access the
command-line tool.

To develop on nycdb itself:

* You can run `pytest` to run the test suite.
* Any changes you make to the tool's source code will automatically be reflected
  in future invocations of `nycdb` and/or the test suite.
* If you don't have a desktop Postgres client, you can always run
  `nycdb --dbshell` to interactively inspect the database with [`psql`][].

You can leave the bash shell with `exit`.

If you ever want to wipe the database, run `docker-compose down -v`.

[install Docker]: https://www.docker.com/get-started
[`psql`]: http://postgresguide.com/utilities/psql.html

###  Adding New Datasets

See the [guide Here](ADDING_NEW_DATASETS.md) for the steps to add a new dataset
