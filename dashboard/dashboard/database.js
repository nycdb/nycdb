const Promise = require('bluebird');
const pgp = require('pg-promise')({ promiseLib: Promise });
const defaultConnectionStr = 'postgres://postgres:nycdb@127.0.0.1:5432/postgres';
const isObjectLike = require('lodash/isObjectLike');
const toString = require('lodash/toString');

const query = require('./query');

//const db = database('postgres://nycdb:nycdb@127.0.0.1:5432/nycdb')
/**
 * 
 * @param {Object|String} boardNumberOrObject
 * @return {Object} { cd: communityBoardString }
 */
const districtObject = function(boardNumberOrObject) {
  if (isObjectLike(boardNumberOrObject)) {
    return {cd: toString(boardNumberOrObject.cd) };
  } else {
    return {cd: toString(boardNumberOrObject) };
  }
};


/**
 * 
 * @param {String} queryName
 * @param {Object|String|Integer} district
 * @returns {String} sqlquery
 */
const queryForDistrict = function(queryName, district) {
  let dObj =  districtObject(district);
  return query[queryName](dObj);
};


/**
 * Returns a function, that when called with a pg connection string,
 * retuns object with queries for each community board.
 * See query.js and the folder sql for more information on the queries.
 *
 * Example use:
 * const db = database('postgres://user:password@127.0.0.1:5432/database')
 * db.recentSales('101') // return Promise
 * 
 * @param {String} defaultConnectionStr
 * @returns {function} 
 */
const database = function(connectionStr = defaultConnectionStr) {
  // Documentation for pg-promise: http://vitaly-t.github.io/pg-promise/
  const db = pgp(connectionStr);

  return {
    _db: db,
    stats: (d) => db.query(queryForDistrict('stats', d)),
    openViolations: (d) => db.query(queryForDistrict('openViolations', d)),
    hpdViolations: (d) => db.query(queryForDistrict('hpdViolations', d)),
    recentSales: (d) => db.query(queryForDistrict('recentSales', d)),
    newBuildingJobs: (d) => db.query(queryForDistrict('newBuildingJobs', d))
  };

};


// private API for testing
database._districtObject = districtObject;
database._queryForDistrict = queryForDistrict;
  
module.exports = database;



