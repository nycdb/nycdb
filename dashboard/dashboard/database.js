const Promise = require('bluebird');
const pgp = require('pg-promise')({ promiseLib: Promise });
const defaultConnectionStr = 'postgres://postgres:nycdb@127.0.0.1:5432/postgres';

module.exports = (cn = defaultConnectionStr) => pgp(cn);

