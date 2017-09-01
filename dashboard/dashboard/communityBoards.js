const fs = require('fs');
const path = require('path');
const pug = require('pug');
// lodash
const identity = require('lodash/identity');
const reduce = require('lodash/reduce');
const merge = require('lodash/merge');
const round = require('lodash/round');
const partial = require('lodash/partial');
const partialRight = require('lodash/partialRight');
// other utils:
const Promise = require("bluebird");
const format = require('d3-format').format;
// helper modules
const db = require('./database')();
const sql = require('./query');
// Compile the pug template into a func
const communityBoardTemplate = pug.compileFile(path.join(__dirname, 'templates', 'communityBoard.pug'), {}); 
// commmunity board data
const communityBoards = require('./community_boards.json');

// converts array returns by stats.sql query into an object
const flatMerge = (results, original = {}) => {
  return reduce(results, (acc, val) => merge(acc, { [val.name]: val.d }), original);
};

const parseViolations = result => (
  {
    "violationBuildings": result[0].buildings,
    "numberOfViolations": result[0].number_of_violations
  }
);

// [] -> []
// Formats sale.saleprice for better readability
const formatSales = sales => {
  return sales.map(sale => merge(sale, {saleprice: format('$,')(sale.saleprice) }));
};

// wraps values in an object, and optionally transforms the values
// example: wrap([1,2,3] ,'numbers', x => x.map(x => x * 2)) => { "numbers": [2,4,6]}
const wrap = (values, key, transformation = identity) => {
  return { [key]: transformation(values) };
};

// input: String, String, Function
// output: Promise
// Returns promise for district/ queryName combination
const query = (district, queryName, thenFunc) => {
  let cdObj = {cd: district};
  return db.query(sql[queryName](cdObj)).then(thenFunc);
};

// queries and a callback
const queries = [
  [ 'stats', flatMerge ],
  [ 'openViolations', parseViolations ],
  [ 'recentSales', (sales) => wrap(sales, 'recentSales', formatSales)  ],
  [ 'newBuildingJobs', (jobs) => wrap(jobs, 'newBuildingJobs') ]
];


// str -> array of Promises
const executeQueries = (district) => {
  let queryForDistrict = partial(query, district);
  return queries.map( q => queryForDistrict(...q) );
};

// str => Promise
const queriesPromise = (district) => {
  return Promise.all(executeQueries(district));
};

// return values by the queries promise
// in to a single object
// array, str -> object
const processValues = (data, district) => {
  return reduce(data, (acc, val) => merge(acc, val), {cd: district});
};

const calculateViolationStats = (values) => {
  return merge(values, {
    "violationsPerUnit": round(values.numberOfViolations / values.unitsres, 2),
    "resBuildingsWithViolationsPct": format(".1%")((values.violationBuildings / values.buildingsres))
  });
};

const saveFile = (district, html, folder) => {
  fs.writeFileSync(`${folder}/${district}.html`, html);
};

// Str, Str -> Promise
// Retrives data for district and generates html document
const generateCdHtml = (district) => {
  return queriesPromise(district)
    .catch( err => console.error(err) )
    .then( values => { console.log(`Processing: ${district}`); return values; })
    .then( values => processValues(values, district))
    .then(calculateViolationStats)
    .then(communityBoardTemplate)
    .then( html => saveFile(district, html, './public'));
    
};

const main = () => {
  let districts = communityBoards
      .map( communityBoard => communityBoard.cd );
  
  Promise
    .map(districts, generateCdHtml, {concurrency: 2})
    .catch((err) => {
      console.error('something went wrong');
      console.error(err);
    })
    .then(() => console.log('Completed'));
};

module.exports = main;
