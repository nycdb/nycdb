#!/usr/bin/env node
const communityBoards = require("./dashboard/communityBoards.js");

const helpCommands = [ 'help', '-help', '--help', '-h'];

const help = `
Community Board Json
   use: community-board-json [PostgresConnectionString]

Outputs json array of community boards with statistical information.

Requires running instance of nycd-db. The default connection 
string is 'postgres://postgres:nycdb@127.0.0.1:5432/postgres'
`;

const arg = process.argv[2];

if (helpCommands.includes(arg)) {
  console.error(help);
} else {

  communityBoards.main(arg)
    .then( results => process.stdout.write(JSON.stringify(results)));
  
}
