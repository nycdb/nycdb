cd "tests/integration/data"

mkdir -p "nyc-zip-codes"
pgsql2shp -f "nyc-zip-codes/ZIP_CODE_040114.shp" -h "host.docker.internal" -p "5432" -u "nycdb" -P "nycdb" "nycdb" "select * from zipcodes limit 5"
zip -r "nyc-zip-codes.zip" "nyc-zip-codes"
rm -rf "nyc-zip-codes"
