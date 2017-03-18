#!/bin/bash

# This demostrates how to setup a server with fresh install of Ubuntu 14.04 or Debian Jessie, with postgres running locally

# Inital update & upgrade
apt-get update && apt-get upgrade

# Install requirements & postgres
apt-get install build-essential wget python3 python3-dev python3-psycopg2 python3.4-venv postgresql-client unzip git postgresql postgresql-contrib

# Log in as postgres user
su - postgres
# create new postgres superuser
createuser -d -P --superuser nycdb_pguser
# enter nycdb_pguser's password
# create the database
createdb nycdb
exit # leave postgres user shell

# verify that the postgres connection works:
psql -U nycdb_pguser -h 127.0.0.1 -d nycdb

# clone repo
git clone https://github.com/aepyornis/nyc-db.git --recursive
cd nyc-db
# copy and edit env.sh
cp env.sh.sample env.sh
nano env.sh  # 
# env.sh 
# export PGPASSWORD=password # whatever password as entered in above
# execute_sql () {
#  psql -h 127.0.0.1 -d nycdb -U nycdb_pguser -f $1
# }

# execute_sql_cmd () {
#  psql -h 127.0.0.1 -d nycdb -U nycdb_pguser --command "$1"
# }

# NYCDB_CONNECTION_STRING="dbname=nycdb user=nycdb_user password=password host=127.0.0.1"# 
#


# Probaby not needed, but if the files happen to not be executable: 
# chmod +x ./nyc_db.sh && chmod +x ./download.sh

# download the data:
./download.sh all
# create postgres database
./nyc_db.sh
