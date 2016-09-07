import re
import unittest

from mock import Mock
import httpretty

from optimoveapi.transport import Transport
from optimoveapi.exceptions import (
    ExpiredToken,
    OptimoveError,
)

from .constants import BASE_URL


@httpretty.activate
class TransportRequestTests(unittest.TestCase):

    def setUp(self):
        self.transport = Transport(BASE_URL, 'username', 'password')

    def test_expired_token(self):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/category/listResource',
            body='Authorization-Token Expired',
            status=403,
        )
        with self.assertRaises(ExpiredToken):
            self.transport._request('post', 'category/listResource')

    def test_optimove_internal_error(self):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/category/listResource',
            body='Plain text message',
            status=500,
        )
        with self.assertRaises(OptimoveError):
            self.transport._request('post', 'category/listResource')

    def test_bad_json_returned(self):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/category/listResource',
            body='',
            status=200,
            content_type='application/json',
        )
        with self.assertRaises(OptimoveError):
            self.transport._request('post', 'category/listResource')


@httpretty.activate
class TransportAuthorizedRequestTests(unittest.TestCase):

    def setUp(self):
        self.transport = Transport(BASE_URL, 'username', 'password')

    @staticmethod
    def token_logic(request, uri, headers):
        """Simulates Optimove's logic around authorization token.
        Handles:
        * Logging-in: Returns valid token.
        * Getting resource with expired token: Returns 403.
        * Getting resource with valid token: Returns 200.
        """
        if uri.endswith('general/login'):
            return 200, headers, '"valid_token"'
        auth_header = request.headers.get('authorization-token')
        if auth_header == 'expired_token':
            return 403, headers, 'Authorization-Token Expired'
        if auth_header == 'valid_token':
            return 200, headers, '["asd"]'
        raise ValueError

    def test_request_without_token(self):
        callback_mock = Mock(side_effect=self.token_logic)
        httpretty.register_uri(
            method=httpretty.POST,
            uri=re.compile(BASE_URL + '/(.*)'),
            body=callback_mock,
        )
        body = self.transport._authorized_request(
            'post', 'category/asdListResource'
        )
        assert body == ['asd']
        assert callback_mock.call_count == 2

    def test_request_with_expired_token(self):
        # To get data with expired token 3 requests will be made:
        # 1. Get resource. Response will tell "token has expired",
        # 2. Refresh token (login),
        # 3. Get resource again that returns expected data.
        callback_mock = Mock(side_effect=self.token_logic)
        httpretty.register_uri(
            method=httpretty.POST,
            uri=re.compile(BASE_URL + '/(.*)'),
            body=callback_mock,
        )
        # Save "expired" in used headers
        self.transport._session.headers[Transport.AUTH_HEADER] = (
            'expired_token'
        )
        body = self.transport._authorized_request(
            'post', 'category/asdListResource'
        )
        assert body == ['asd']
        assert callback_mock.call_count == 3
