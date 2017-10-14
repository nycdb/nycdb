#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const pagesMaker = require("./dashboard/communityBoardPagesMaker.js");

const helpCommands = [ 'help', '-help', '--help', '-h'];

const DEFAULT_OUTPUT_FOLDER = './public';

const help = `
Community Board Pages: creates community board website
  use: commmunity-board-pages COMMUNITY-BOARD-JSON-FILE
`;

const makeDirIfNotExists = function(dir) {
  if (!fs.existsSync(dir)){
    fs.mkdirSync(dir);
  }
};

const copyCss = (dir) => {
  fs.copyFileSync(
    path.join(__dirname, 'node_modules/tachyons/css/tachyons.min.css'),
    path.join(dir, 'tachyons.css')
  );

  fs.copyFileSync(
    path.join(__dirname, 'dashboard', 'styles.css'),
    path.join(dir, 'styles.css')
  );

};


if (helpCommands.includes(process.argv[2])) {
  
  console.error(help);
  
} else {
  
  let pathToJson = path.resolve(process.argv[2]);
  let folder = process.argv[3] || DEFAULT_OUTPUT_FOLDER;

  makeDirIfNotExists(folder);
  copyCss(folder);
  pagesMaker(require(pathToJson), folder);
  
}
