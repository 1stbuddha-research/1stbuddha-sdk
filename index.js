const ORIGIN = 'https://1stbuddha.com';

export class CatalogError extends Error {
  constructor(status, detail, retryAfter = null) {
    super(`1stBuddha HTTP ${status}: ${detail}`);
    this.name = 'CatalogError';
    this.status = status;
    this.retryAfter = retryAfter;
  }
}

/** Public catalog reads only. No credentials, cart, reservation or checkout operations. */
export class FirstBuddha {
  constructor({fetch: fetcher = globalThis.fetch, timeout = 15000} = {}) {
    if (typeof fetcher !== 'function') throw new TypeError('A fetch implementation is required.');
    if (!Number.isFinite(timeout) || timeout < 1 || timeout > 60000) throw new TypeError('Timeout must be between 1 and 60000 ms.');
    this.fetcher = fetcher;
    this.timeout = timeout;
  }

  async read(path, markdown = false) {
    const response = await this.fetcher(ORIGIN + path, {
      method: 'GET', credentials: 'omit', redirect: 'error',
      headers: {Accept: markdown ? 'text/markdown' : 'application/json'},
      signal: AbortSignal.timeout(this.timeout)
    });
    const body = await response.text();
    if (!response.ok) {
      let detail = response.statusText || 'Public request failed';
      try {const problem = JSON.parse(body); detail = problem.detail || problem.message || detail;} catch {}
      throw new CatalogError(response.status, detail, response.headers.get('Retry-After'));
    }
    return markdown ? body : JSON.parse(body);
  }

  product(handle) {
    if (typeof handle !== 'string' || handle.length > 250 || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(handle)) throw new TypeError('Use the exact handle from a current product URL.');
    return this.read('/api/v1/products/' + handle);
  }

  async search(query) {
    if (typeof query !== 'string' || !query.trim() || query.length > 150) throw new TypeError('Search query must contain 1 to 150 characters.');
    const result = await this.read('/search/suggest.json?q=' + encodeURIComponent(query.trim()) + '&resources[type]=product&resources[limit]=10');
    return result.resources?.results?.products || [];
  }

  discover() {return this.read('/openapi.json');}
  guide() {return this.read('/llms.txt', true);}
}
