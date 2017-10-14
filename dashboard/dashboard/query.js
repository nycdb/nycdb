const fs = require('fs');
const template = require('lodash/template');
const path = require('path');

const sqlFile = file => {
  return fs.readFileSync(path.join(__dirname, 'sql', `${file}.sql`));
};

const sqlQuery = file => template(sqlFile(file));

// These functions are lodash template that take one argument: an attributes object
// The object needs to contain the the key 'cd' with the community board number
// The functions return a SQL string
// Example:
//   require('query').recentSales({cd: '101'})
module.exports = {
  stats: sqlQuery('stats'),
  recentSales: sqlQuery('recent_sales'),
  newBuildingJobs: sqlQuery('new_building_jobs'),
  hpdViolations: sqlQuery('hpd_violations'),
  dobjobs: sqlQuery('dob_jobs')
};
