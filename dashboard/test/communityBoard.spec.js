require('chai/register-expect');

const communityBoard = require('../dashboard/communityBoards.js');

// describe('Array', function() {
//   describe('#indexOf()', function() {
//     it('should return -1 when the value is not present', function() {
//       expect(-1).to.equal([1,2,3].indexOf(4));
//     });
//   });
// });


describe('jsonForBoardPromise', function(){

  let district = { cd: '101' };

  it("returns a promise", function() {
    expect(communityBoard.jsonForBoardPromise(district))
      .to.be.a('promise');
  });
  

});
