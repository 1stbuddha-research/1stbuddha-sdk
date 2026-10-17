# Official 1stBuddha catalog clients

Source for the JavaScript and Python public catalog clients at https://1stbuddha.com.

**Release status:** source published; registry releases pending account verification. Installation commands below apply after the corresponding registry release is published.

## JavaScript SDK and CLI

Official dependency-free client for the public 1stBuddha catalog of antique Buddha statues and Asian art. Public catalog access requires no signup or API key.

### Install

```sh
npm install 1stbuddha
```

```js
import {FirstBuddha} from '1stbuddha';
const catalog = new FirstBuddha();
const matches = await catalog.search('bronze Buddha');
const product = await catalog.product('large-japanese-amida-buddha-statue');
```

```sh
npx 1stbuddha search bronze Buddha
npx 1stbuddha product large-japanese-amida-buddha-statue
npx 1stbuddha discover
```

Requires Node.js 20 or newer.

Read the exact current product handle from a storefront URL. Product responses retain the native API fields, currency and price units; do not assume that a numeric price is expressed in whole euros. Recheck availability before purchase. A search response is not a reservation.

These clients make public GET requests only. They accept no credentials, do not persist cookies, refuse redirects and cannot create orders or access customer accounts. Network and API errors are surfaced to the caller; HTTP errors preserve status and Retry-After where supplied. No automatic retries.

Official documentation: https://1stbuddha.com/developers
OpenAPI: https://1stbuddha.com/openapi.json
License: MIT for this client code only. Product text, research and images are not licensed by this package.

## Python SDK and CLI

Official dependency-free client for the public 1stBuddha catalog of antique Buddha statues and Asian art. Public catalog access requires no signup or API key.

### Install

```sh
pip install 1stbuddha
```

```python
from firstbuddha import FirstBuddha
catalog = FirstBuddha()
matches = catalog.search("bronze Buddha")
product = catalog.product("large-japanese-amida-buddha-statue")
```

```sh
firstbuddha search bronze Buddha
firstbuddha product large-japanese-amida-buddha-statue
firstbuddha discover
```

Requires Python 3.9 or newer.

Read the exact current product handle from a storefront URL. Product responses retain the native API fields, currency and price units; do not assume that a numeric price is expressed in whole euros. Recheck availability before purchase. A search response is not a reservation.

These clients make public GET requests only. They accept no credentials, do not persist cookies, refuse redirects and cannot create orders or access customer accounts. Network and API errors are surfaced to the caller; HTTP errors preserve status and Retry-After where supplied. No automatic retries.

Official documentation: https://1stbuddha.com/developers
OpenAPI: https://1stbuddha.com/openapi.json
License: MIT for this client code only. Product text, research and images are not licensed by this package.

## Tests

`node --test test.mjs` and `python -m unittest test_client.py`.
