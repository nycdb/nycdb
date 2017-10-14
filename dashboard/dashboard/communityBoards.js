const Promise = require("bluebird");
const query = require('./query');
const database = require('./database');
const partial = require('lodash/partial');
const reduce = require('lodash/reduce');
const merge = require('lodash/merge');
const identity = require('lodash/identity');
const cloneDeep = require('lodash/cloneDeep');

// commmunity board data
const communityBoardList = require('./community_boards.json');
const queries = [ 'stats', 'recentSales','newBuildingJobs', 'hpdViolations' ];

const CONCURRENCY = 3;

/**
 * wraps values in an object, and optionally transforms the values
 * 
 * example: wrap('numbers', [1,2,3], x => x.map(x => x * 2)) => { "numbers": [2,4,6]}
 * @param {String} key
 * @param {Any} values
 * @param {[Function]} optional transformation function
 * @returns {Object} 
 */
const wrap = (key, values, transformation = identity) => {
  return { [key]: transformation(values) };
};

/**
 * Promise for a single community board
 * 
 *
 * @param {Database} database instance
 * @param {Object} district
 * @returns {Promise}
 */
const jsonForBoardPromise = function(db, district) {
  return Promise
    .all(queries.map( queryName => {
      return db[queryName](district).then( values => wrap(queryName, values) );
    }))
    .then( values => values.concat([ wrap('district', district)]) )
    .then( values => reduce(values, (acc, val) => merge(acc, val) ) )
    .then( values => { console.error(`Processed: ${district.cd}`); return values; });
};

/**
 * Returns a promise that, if sucuesfully resolved,
 * will contain the acculated stats for the community board
 * 
 * @param {String} [Postgres Connection String]
 * @returns {Promise} 
 */
const main = function(cs = 'postgres://nycdb:nycdb@127.0.0.1:5432/nycdb') {
  const db = database(cs);
  var boards = communityBoardList; // .slice(0,2);
  return Promise
    .map(boards, partial(jsonForBoardPromise, db), { concurrency: CONCURRENCY });
};

module.exports = {
  "jsonForBoardPromise": jsonForBoardPromise,
  "_wrap": wrap,
  "main": main,
  "queries": () => cloneDeep(queries)
};
