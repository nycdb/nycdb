require('chai/register-expect');
const sinon = require('sinon');
const reduce = require('lodash/reduce');
const merge = require('lodash/merge');
const Promise = require("bluebird");

const communityBoards = require('../dashboard/communityBoards.js');

describe('wrap', function(){

  it('wraps values in an object', function() {
    expect(communityBoards._wrap('numbers', [1,2,3])).to.deep.equal({ "numbers": [1,2,3] });
  });

  it('wraps values in an object and accept a transofmation function', function() {
    expect(communityBoards._wrap('numbers', [1,2,3], x => x.map(x => x * 2))).to.deep.equal({ "numbers": [2,4,6] });
  });
});


describe('jsonForBoardPromise', function(){

  it('calls db with the query, district, and wraps the return values', function(){

    const mockDb = reduce(
      communityBoards.queries(),
      (acc, query, i) => merge(acc, { [query]: (x) => Promise.resolve(([1,2,3]) ) }),
      {}
    ); 

    const jsonPromise = communityBoards.jsonForBoardPromise(mockDb, { cd: '101' });

    jsonPromise
      .then( values => {

	expect(values).to.deep.equal({
	  "stats": [1,2,3],
	  "openViolations": [1,2,3],
	  "recentSales": [1,2,3],
	  "newBuildingJobs": [1,2,3],
	  "hpdViolations": [1,2,3],
	  "district": { "cd": '101' }
	});
	
      });
  });
  
});

