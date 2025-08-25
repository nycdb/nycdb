# Create zip folder of test data for a specific pluto version.

# First copy the YML file for the previous PLUTO version, update the name
# everywhere for the new version, and add the new URL. Then enter the docker
# container (docker-compose run --entrypoint bash nycdb) and run "nycdb
# --download" for the new pluto version. Now while still within the docker
# container, from the src/ directory, run this file to create the new test data.
# Then add a new test to tests/test_nycdb.py, then exit the docker container and
# run "sh scripts/test" to run all the tests.

VERSION=25v2_1

DATA_DIR="data"
TEST_DIR="tests/integration/data"

mkdir -p "${TEST_DIR}/pluto_${VERSION}"
unzip -d "${DATA_DIR}" "${DATA_DIR}/pluto_${VERSION}.zip"
head -n 6 "${DATA_DIR}/pluto_${VERSION}.csv" > "${TEST_DIR}/pluto_${VERSION}/pluto_${VERSION}.csv"
zip -r "${TEST_DIR}/pluto_${VERSION}.zip" "${TEST_DIR}/pluto_${VERSION}"
rm -rf "${TEST_DIR}/pluto_${VERSION}"

