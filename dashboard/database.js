// const initOptions = {}
const pgp = require('pg-promise')({});
const defaultConnectionStr = 'postgres://postgres:nycdb@127.0.0.1:5432/postgres';

module.exports = (cn = defaultConnectionStr) => pgp(cn);

