#!/bin/bash

source env.sh

cd $RENTSTAB_REPO

python3 insert_rentstab.py $RENTSTAB_FILE "${NYCDB_CONNECTION_STRING}"
