const fs = require('fs');
const template = require('lodash/template');

const sqlFile = file => fs.readFileSync(`sql/${file}.sql`);

module.exports = {
  stats: template(sqlFile('stats')),
  openViolations: template(sqlFile('open_violations')),
  recentSales: template(sqlFile('recent_sales'))
};
