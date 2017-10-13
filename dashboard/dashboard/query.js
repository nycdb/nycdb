const fs = require('fs');
const template = require('lodash/template');
const path = require('path');

const sqlFile = file => {
  return fs.readFileSync(path.join(__dirname, 'sql', `${file}.sql`));
};

const sqlQuery = file => template(sqlFile(file));


// These functions are lodash template that take one argument: a attributes object
// The come needs to contain the the key 'cd' with the community board number
// They output a sql string
// require('query').openViolations({cd: '101'})
module.exports = {
  stats: sqlQuery('stats'),
  openViolations: sqlQuery('open_violations'),
  recentSales: sqlQuery('recent_sales'),
  newBuildingJobs: sqlQuery('new_building_jobs'),
  hpdViolations: sqlQuery('hpd_violations')
};
