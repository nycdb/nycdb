#!/bin/bash

cat <<EOF
export PGPASSWORD=${DB_PASSWORD}

execute_sql () {
 psql -h ${DB_HOST} -d ${DB_DATABASE} -U ${DB_USER} -f "\$1"
}

execute_sql_cmd () {
 psql -h ${DB_HOST} -d ${DB_DATABASE} -U ${DB_USER} --command  "\$1"
}
EOF
