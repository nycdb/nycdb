const pug = require('pug');
const fs = require('fs');
const cd = require('./cd');
const reduce = require('lodash/reduce');
const merge = require('lodash/merge');
const round = require('lodash/round');
const cdFn = pug.compileFile('./src/cd.pug',{}); // Compile the pug into func
const db = cd.db();

const districts = [ '303', '304'];

const flatMerge = (results, original = {}) => {
  return reduce(results, (acc, val) => merge(acc, { [val.name]: val.d }), original);
};

const parseViolations = result => ({'violationBuildings': result[0].buildings, 'numberOfViolations': result[0].number_of_violations });

// TODO: formatNum
const parseSales = sales => {
  return sales.map(sale => merge(sale, {salePrice: formatNum(salePrice)}));
}

const generateCdHtml = (district) => {
  let cdObj = {cd: district};

  return Promise.all( [
    db.query(cd.sqlFn.stats(cdObj)).then(flatMerge),
    db.query(cd.sqlFn.openViolations(cdObj)).then(parseViolations),
    db.query(cd.sqlFn.recentSales(cdObj)).then( sales => ({recentSales: sales}))
  ])
    .then( values => reduce(values, (acc, val) => merge(acc, val), cdObj))
    .then( values => merge(values, { 'violationsPerUnit': round(values.numberOfViolations / values.unitsres, 2) }))
    .then(cdFn)
    .then( html => fs.writeFileSync(`public/${district}.html`, html));
};
	
Promise.all( districts.map(generateCdHtml) )
  .then( () => console.log('finished generating files'), err => console.error(err));






