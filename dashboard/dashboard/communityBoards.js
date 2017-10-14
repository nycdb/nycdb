const Promise = require("bluebird");
const query = require('./query');
const database = require('./database');

const partial = require('lodash/partial');
const reduce = require('lodash/reduce');
const merge = require('lodash/merge');
const identity = require('lodash/identity');
const cloneDeep = require('lodash/cloneDeep');
const isNumber = require('lodash/isNumber');
const toNumber = require('lodash/toNumber');


// commmunity board data
const communityBoardList = require('./community_boards.json');
const queries = [ 'stats', 'recentSales','newBuildingJobs', 'hpdViolations' ];

const CONCURRENCY = 3;

const toN = (n) => isNumber(n) ? n : toNumber(n.replace(',', '').replace('$', ''));

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
 * Adds additional statistics for the community board
 *
 * @param {Object} json
 * @returns {Object} 
 */
const computeStats = function(json) {
  let stats = {
    "openViolationsPerUnit": toN(json.stats.totalNumberOfOpenViolations) / toN(json.stats.unitsres),
    "openViolationsPerBuilding": toN(json.stats.totalNumberOfOpenViolations) / toN(json.stats.buildingsres)
  };
  return merge(json, { "stats": stats } );
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
  const execQuery = (queryName) => db[queryName](district).then( values => wrap(queryName, values) );

  return Promise 
    .all(queries.map(execQuery))
    .then( values => values.concat([ wrap('district', district)]) )
    .then( values => reduce(values, (acc, val) => merge(acc, val) ) )
    .then( values => computeStats(values) )
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
  "computeStats": computeStats,
  "queries": () => cloneDeep(queries)
};
