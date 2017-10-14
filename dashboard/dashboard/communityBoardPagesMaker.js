const fs = require('fs');
const path = require('path');
const pug = require('pug');

const mapValues = require('lodash/mapValues');
const groupBy = require('lodash/groupBy');
const toPairs = require('lodash/toPairs');
const merge = require('lodash/merge');
const round = require('lodash/round');

const format = require('d3-format').format;
const toN = require('./toN');

// commmunity board data
const communityBoardsData = require('./community_boards.json');

const DEFAULT_OUTPUT_FOLDER = './public';

const saveFile = (fileName, html, folder = DEFAULT_OUTPUT_FOLDER) => {
  fs.writeFileSync(`${folder}/${fileName}.html`, html);
};

/**
 * Formats and generates stats values for the template
 * @param {Object} stats
 * @returns {Ojbect} stats
 */
const statsPresenter = (stats) => {
  let numericStats = mapValues(stats, toN);
  let formattedStats = {
    "openViolationsPerUnit": round( numericStats.openViolationsPerUnit,  2).toString() ,
    "resBuildingsWithViolationsPct": format(".1%")( ( numericStats.buildingsWithOpenViolations / numericStats.buildingsres) )
  };
  
  let statsWithComma = mapValues(stats, stat => format(',')(toN(stat)));
  return merge(statsWithComma, formattedStats);
};

//compiled pug templates
const communityBoardTemplate = pug.compileFile(path.join(__dirname, 'templates', 'communityBoard.pug'), {});
const indexTemplate = pug.compileFile(path.join(__dirname, 'templates', 'index.pug'));


const index = () => {
  // data structure: [ 'Bronx'. [ {}, {} ] ]
  let districtData = { districts: toPairs(groupBy(communityBoardsData, 'borough')) };
  let html = indexTemplate(districtData);
  saveFile('index', html);
};


/**
 * Turn array of information about community boards and saves them as files
 * @param {Array[Objects]} communityBoardsJson
 */
const main = (communityBoardsJson) => {
  index();
  
  communityBoardsJson
    .map( board => merge(board, {stats: statsPresenter(board.stats) }) )
    .map( board => ( { fileName: board.district.cd, html: communityBoardTemplate(board) } ) )
    .forEach( ({fileName, html}) => saveFile(fileName, html) );
};

main._statsPresenter = statsPresenter;

module.exports = main;
