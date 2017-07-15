// const initOptions = {}
const fs = require('fs');
const pgp = require('pg-promise')({});
const template = require('lodash/template');
const defaultConnectionStr = 'postgres://postgres:nycdb@127.0.0.1:5432/postgres';

const sqlFile = file => fs.readFileSync(`sql/${file}.sql`);

const sqlFn = {
  stats: template(sqlFile('stats')),
  openViolations: template(sqlFile('open_violations')),
  recentSales: template(sqlFile('recent_sales'))
};

module.exports = {
  db: (cn = defaultConnectionStr) => pgp(cn),
  sqlFn: sqlFn
};
