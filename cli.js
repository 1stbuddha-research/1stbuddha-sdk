#!/usr/bin/env node
import {FirstBuddha} from './index.js';
const [command, ...values] = process.argv.slice(2);
const client = new FirstBuddha();
try {
  let result;
  switch(command) {
    case 'product': result = await client.product(values[0]); break;
    case 'search': result = await client.search(values.join(' ')); break;
    case 'discover': result = await client.discover(); break;
    case 'guide': result = await client.guide(); break;
    case undefined: case '--help':
      result = '1stBuddha public catalog CLI\nCommands: search <query>, product <handle>, discover, guide\nPublic reads require no signup or API key. No purchases or reservations.'; break;
    default: throw new Error('Unknown command; use --help.');
  }
  console.log(typeof result === 'string' ? result : JSON.stringify(result, null, 2));
} catch(error) {console.error(error.message); process.exitCode = 1;}
