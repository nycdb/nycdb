const isNumber = require('lodash/isNumber');
const toNumber = require('lodash/toNumber');

module.exports = (n) => {
  return isNumber(n) ? n : toNumber(n.replace(',', '').replace('$', ''));
};


