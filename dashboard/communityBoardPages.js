#!/usr/bin/env node
const path = require('path');
const pagesMaker = require("./dashboard/communityBoardPagesMaker.js");

const helpCommands = [ 'help', '-help', '--help', '-h'];

const help = `
Community Board Pages: creates community board website
  use: commmunity-board-pages COMMUNITY-BOARD-JSON-FILE
`;

const arg = process.argv[2];

if (helpCommands.includes(arg)) {
  console.error(help);
} else {
  pagesMaker(require(path.resolve(arg)));
}
