const fs = require('fs');
const template = require('lodash/template');
const path = require('path');

const sqlFile = file => {
  return fs.readFileSync(path.join(__dirname, 'sql', `${file}.sql`));
};

const sqlQuery = file => template(sqlFile(file));

module.exports = {
  stats: sqlQuery('stats'),
  openViolations: sqlQuery('open_violations'),
  recentSales: sqlQuery('recent_sales'),
  newBuildingJobs: sqlQuery('new_building_jobs'),
  hpdViolations: sqlQuery('hpd_violations')
};