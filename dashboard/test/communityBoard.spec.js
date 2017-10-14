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

const statsFromDb =  {
  "unitsres": "100",
  "buildingsres": "10",
  "totalNumberOfOpenViolations": "50"
};

const statsWithComputedStats = {
  "unitsres": "100",
  "buildingsres": "10",
  "totalNumberOfOpenViolations": "50",
  "openViolationsPerUnit": 0.5,
  "openViolationsPerBuilding": 5
};


describe('computeStats', function(){
  const json = {
    "stats": statsFromDb,
    "recentSales": [1,2,3]
  };

  const computedStats = communityBoards.computeStats(json).stats;

  it('retains original values', function(){
    expect(communityBoards.computeStats(json).recentSales).to.deep.equal([1,2,3]);

    for (var prop in json.stats) {
      expect(computedStats).to.have.property(prop);
    }
  });

  it("cacluates violationsPerUnit", function(){
    expect(computedStats.openViolationsPerUnit).to.equal(0.5);
  });
    

  it('caculates violationsPerBuilding', function(){
    expect(computedStats.openViolationsPerBuilding).to.equal(5);
  });
  
});


describe('jsonForBoardPromise', function(){

  const promiseFor = function(values) {
    return (district) => Promise.resolve(values);
  };

  it('calls db with the query, district, and wraps the return values', function(){
    const mockDb = {
      "stats": promiseFor({"unitsres": "100", "buildingsres": "10", "totalNumberOfOpenViolations": "50"}),
      "recentSales": promiseFor([1,2,3]),
      "newBuildingJobs": promiseFor([1,2,3]),
      "hpdViolations": promiseFor([1,2,3])
    };

    const jsonPromise = communityBoards.jsonForBoardPromise(mockDb, { cd: '101' });

    jsonPromise
      .then( values => {

	expect(values).to.deep.equal({
	  "stats": statsWithComputedStats,
	  "recentSales": [1,2,3],
	  "newBuildingJobs": [1,2,3],
	  "hpdViolations": [1,2,3],
	  "district": { "cd": '101' }
	});
	
      });
  });
  
});

