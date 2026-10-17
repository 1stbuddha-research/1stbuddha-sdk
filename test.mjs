import {test} from 'node:test';
import assert from 'node:assert/strict';
import {FirstBuddha, CatalogError} from './index.js';
test('Product handle cannot change destination; public reads omit credentials and refuse redirects', async () => {
 const requests = [];
 const client = new FirstBuddha({fetch: async (url, options) => {requests.push({url,options});return new Response('{"title":"Buddha","price":10000}');}});
 for (const handle of ['../account', 'https://evil.example', 'foo?secret=1', '', 'x'.repeat(251)]) assert.throws(() => client.product(handle));
 assert.equal(requests.length, 0);
 assert.equal((await client.product('bronze-buddha')).title,'Buddha');
 assert.equal(requests[0].url,'https://1stbuddha.com/api/v1/products/bronze-buddha');
 assert.equal(requests[0].options.credentials,'omit');assert.equal(requests[0].options.redirect,'error');
});
test('Search encodes text, bounds input and exposes native result records', async () => {
 let request;
 const client = new FirstBuddha({fetch: async url => {request=url;return new Response('{"resources":{"results":{"products":[{"title":"A","available":false}]}}}');}});
 assert.equal((await client.search('bronze & gold'))[0].available,false);
 assert.match(request,/q=bronze%20%26%20gold/);
 await assert.rejects(client.search(' '));await assert.rejects(client.search('x'.repeat(151)));
});
test('Structured errors retain HTTP status and retry hint without returning an HTML error as data', async () => {
 const client = new FirstBuddha({fetch: async () => new Response('{"detail":"Slow down"}',{status:429,headers:{'Retry-After':'30'}})});
 await assert.rejects(client.discover(), e => e instanceof CatalogError && e.status===429 && e.retryAfter==='30' && /Slow down/.test(e.message));
});
