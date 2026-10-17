import io
import unittest
import urllib.error
from unittest.mock import Mock
from firstbuddha import FirstBuddha, CatalogError, _NoRedirect


class ClientTests(unittest.TestCase):
    def test_invalid_handles_never_reach_network(self):
        client = FirstBuddha()
        client._opener = Mock()
        for handle in ["../account", "https://evil.example", "foo?token=1", "", "x" * 251]:
            with self.assertRaises(ValueError): client.product(handle)
        client._opener.open.assert_not_called()

    def test_product_read_has_no_cookie_or_authorization(self):
        client = FirstBuddha()
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = b'{"title":"Buddha","price":12345}'
        client._opener = Mock()
        client._opener.open.return_value = response
        self.assertEqual(client.product("bronze-buddha")["price"], 12345)
        request = client._opener.open.call_args.args[0]
        self.assertEqual(request.full_url, "https://1stbuddha.com/api/v1/products/bronze-buddha")
        self.assertNotIn("Cookie", request.headers)
        self.assertNotIn("Authorization", request.headers)
        self.assertIsNone(_NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.example"))

    def test_search_encodes_query_and_bounds_input(self):
        client = FirstBuddha()
        client._read = Mock(return_value={"resources":{"results":{"products":[{"available":False}]}}})
        self.assertFalse(client.search("bronze & gold")[0]["available"])
        self.assertIn("q=bronze%20%26%20gold", client._read.call_args.args[0])
        for query in [" ", "x" * 151, None]:
            with self.assertRaises(ValueError): client.search(query)

    def test_error_preserves_status_and_retry_hint(self):
        client = FirstBuddha()
        client._opener = Mock()
        client._opener.open.side_effect = urllib.error.HTTPError("https://1stbuddha.com/openapi.json",429,"Rate limited",{"Retry-After":"30"},io.BytesIO(b'{"detail":"Slow down"}'))
        with self.assertRaises(CatalogError) as caught: client.discover()
        self.assertEqual(caught.exception.status,429)
        self.assertEqual(caught.exception.retry_after,"30")


if __name__ == "__main__": unittest.main()
