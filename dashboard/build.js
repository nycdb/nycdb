const fs = require('fs');
const pug = require('pug');

const format = require('d3-format').format;

// lodash
const reduce = require('lodash/reduce');
const merge = require('lodash/merge');
const round = require('lodash/round');
const partial = require('lodash/partial');
const noop = require('lodash/noop');

const db = require('./database')();
const sql = require('./query');
const cdFn = pug.compileFile('./src/cd.pug',{}); // Compile the pug into func


const districts = [ '303', '304'];

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

// [] => {}
// wraps sales array in an object
const wrapSales = sales => ({"recentSales": formatSales(sales)});

// input: String, String, Function
// output: Promise
// Returns promise for district/ queryName combination
const query = (district, queryName, thenFunc = noop) => {
  let cdObj = {cd: district};
  return db.query(sql[queryName](cdObj)).then(thenFunc);
};

// str -> array of Promises
const queries = (district) => {
  let queryForDistrict = partial(query, district);

  return [
    [ 'stats', flatMerge ],
    [ 'openViolations', parseViolations ],
    [ 'recentSales', wrapSales ]
  ]
      .map( x => queryForDistrict(...x) );
  
};

// str => Promise
const queriesPromise = (district) => {
  return Promise.all(queries(district));
};

// return values by the queries promise
// in to a single object
// array, str -> object
const processValues = (data, district) => {
  return reduce(data, (acc, val) => merge(acc, val), {cd: district});
};

// const calculateViolationsPerUnits = (values) => {
//   return merge(values, { 'violationsPerUnit': round(values.numberOfViolations / values.unitsres, 2) });
// };

const calculateViolationStats = (values) => {
  return merge(values, {
    "violationsPerUnit": round(values.numberOfViolations / values.unitsres, 2),
    "resBuildingsWithViolationsPct": format(".1%")((values.violationBuildings / values.buildingsres))
  });
};

//
// str ->
// Writes files
const generateCdHtml = (district) => {
  queriesPromise(district)
    .catch( err => console.error(err) )
    .then( values => processValues(values, district))
    .then(calculateViolationStats)
//    .then ( values => {console.log(values); return values;} )
    .then(cdFn)
    .then( html => fs.writeFileSync(`public/${district}.html`, html));
    
};


districts.forEach( d => generateCdHtml(d) );
