#!/bin/bash

curl https://data.cityofnewyork.us/api/views/uwyv-629c/rows.csv?accessType=DOWNLOAD > /tmp/hpd_complaints.csv

cat /tmp/hpd_complaints.csv | csvsql --db postgres://nycdb:nycdb@127.0.0.1:5432/nycdb --insert --table hpd_complaints
