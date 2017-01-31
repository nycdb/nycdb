export PGPASSWORD=nycdb

execute_sql () {
 psql -h pg -d postgres -U postgres -f $1
}

execute_sql_cmd () {
 psql -h pg -d postgres -U postgres --command "$1"
}

export NYCDB_CONNECTION_STRING="dbname=postgres user=postgres password=nycdb host=pg"
