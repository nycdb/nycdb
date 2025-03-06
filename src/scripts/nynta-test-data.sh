cd "tests/integration/data"
VERSION=25a

for table in  "nynta2010" "nynta2020"
do 
    mkdir -p "${table}_${VERSION}"
    pgsql2shp -f "${table}_${VERSION}/${table}.shp" -h "host.docker.internal" -p "5432" -u "nycdb" -P "nycdb" "nycdb" "select * from ${table} limit 5"
    zip -r "${table}_${VERSION}.zip" "${table}_${VERSION}"
    rm -rf "${table}_${VERSION}"
done
