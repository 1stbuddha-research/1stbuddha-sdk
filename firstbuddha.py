"""Public, read-only 1stBuddha catalog client. Prices retain native API units."""
import argparse
import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request

ORIGIN = "https://1stbuddha.com"


class CatalogError(Exception):
    def __init__(self, status, detail, retry_after=None):
        super().__init__(f"1stBuddha HTTP {status}: {detail}")
        self.status = status
        self.retry_after = retry_after


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class FirstBuddha:
    def __init__(self, timeout=15):
        if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 0 < timeout <= 60:
            raise ValueError("Timeout must be between 0 and 60 seconds.")
        self.timeout = timeout
        self._opener = urllib.request.build_opener(_NoRedirect())

    def _read(self, path, markdown=False):
        request = urllib.request.Request(ORIGIN + path, headers={
            "Accept": "text/markdown" if markdown else "application/json",
            "User-Agent": "1stbuddha-python/1.0.0 (+https://1stbuddha.com/developers)"
        })
        try:
            with self._opener.open(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            detail = str(error.reason)
            try:
                problem = json.loads(error.read().decode("utf-8"))
                detail = problem.get("detail") or problem.get("message") or detail
            except (ValueError, UnicodeError):
                pass
            raise CatalogError(error.code, detail, error.headers.get("Retry-After")) from error
        return body if markdown else json.loads(body)

    def product(self, handle):
        if not isinstance(handle, str) or len(handle) > 250 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", handle):
            raise ValueError("Use the exact handle from a current product URL.")
        return self._read("/api/v1/products/" + handle)

    def search(self, query):
        if not isinstance(query, str) or not query.strip() or len(query) > 150:
            raise ValueError("Search query must contain 1 to 150 characters.")
        result = self._read("/search/suggest.json?q=" + urllib.parse.quote(query.strip(), safe="") + "&resources[type]=product&resources[limit]=10")
        return result.get("resources", {}).get("results", {}).get("products", [])

    def discover(self):
        return self._read("/openapi.json")

    def guide(self):
        return self._read("/llms.txt", markdown=True)


def main():
    parser = argparse.ArgumentParser(description="Read the public 1stBuddha catalog. No purchases or reservations.")
    parser.add_argument("command", choices=["search", "product", "discover", "guide"])
    parser.add_argument("value", nargs="*")
    args = parser.parse_args()
    client = FirstBuddha()
    try:
        if args.command == "search": result = client.search(" ".join(args.value))
        elif args.command == "product": result = client.product(args.value[0] if args.value else "")
        else: result = getattr(client, args.command)()
    except (CatalogError, ValueError, urllib.error.URLError) as error:
        parser.exit(1, str(error) + "\n")
    print(result if isinstance(result, str) else json.dumps(result, indent=2, ensure_ascii=False))
