# Community District Dashboard

A static site with housing statistics for each community district.

Contains two scripts:

``` community-board-json [NYCDB-CONNECTION-STRING] ``` which outputs a json array of all nyc community boards contain housing statistics and data.

``` community-board-pages COMMUNITY-BOARD-JSON-FILE [FOLDER]``` takes the output of the community-board-json and generates the dashboard html.

## Developer setup:

- Ensure there is a running version of NYCDB (see the main README for instructions)

- Install node modules: ``` npm install ```

If you setup NYCDB  with the default credentials (user: nycdb, pass: nycdb, database: nycdb running on localhost) then you can use the convenience NPM scripts without modifications:

- Create json file: ``` npm run json ```

- Build the  site: ``` npm run build ```

Requirements:
  - postgres
  - nodejs > 8.5

