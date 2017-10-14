require('chai/register-expect');
const pagesMaker = require('../dashboard/communityBoardPagesMaker.js');

describe('statsPresenter', function(){
  let stats = {
    "unitsres": "1000",
    "buildingsres": "10",
    "buildingsWithOpenViolations": "5",
    "totalNumberOfOpenViolations": "50",
    "openViolationsPerUnit": 0.245,
    "openViolationsPerBuilding": 5
  };

  let formattedStats = pagesMaker._statsPresenter(stats);
  
  it('rounds openViolationsPerUnit', function(){
    expect(formattedStats.openViolationsPerUnit).to.equal('0.25');
  });

  it('adds commas', function(){
    expect(formattedStats.unitsres).to.equal('1,000');
  });

  it('calculates percent buildings with violations', function(){
    expect(formattedStats.resBuildingsWithViolationsPct).to.equal('50.0%');
  });
  
});
