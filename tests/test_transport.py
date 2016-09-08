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
class TransportGetPostTests(unittest.TestCase):

    def setUp(self):
        self.transport = Transport(BASE_URL, 'username', 'password')
        # Prepare valid token in client's session
        self.transport._session.headers[Transport.AUTH_HEADER] = 'valid_token'

    def test_get(self):
        httpretty.register_uri(
            method=httpretty.GET,
            uri=BASE_URL + '/category/asdListResource',
            body='["asd"]',
        )
        self.transport.get('category/asdListResource', {'asd': 123})
        request = httpretty.last_request()
        assert request.path == '/category/asdListResource?asd=123'
        assert request.body == ''

    def test_post(self):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/category/asdListResource',
            body='["asd"]',
        )
        self.transport.post('category/asdListResource', {'asd': 123})
        request = httpretty.last_request()
        assert request.path == '/category/asdListResource'
        assert request.body == '{"asd": 123}'


@httpretty.activate
class TransportRequestTests(unittest.TestCase):

    def setUp(self):
        self.transport = Transport(BASE_URL, 'username', 'password')

    def test_ok(self):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/category/asdListResource',
            body='["asd"]',
            status=200,
        )
        body = self.transport._request('post', 'category/asdListResource')
        assert body == ['asd']

    def test_expired_token_response(self):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/category/listResource',
            body='Authorization-Token Expired',
            status=403,
        )
        with self.assertRaises(ExpiredToken):
            self.transport._request('post', 'category/listResource')

    def test_internal_error_response(self):
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

    def test_valid_token(self):
        """Get resource with valid token.

        Simulate that token was obtained before.
        """
        callback_mock = Mock(side_effect=self.token_logic)
        httpretty.register_uri(
            method=httpretty.POST,
            uri=re.compile(BASE_URL + '(.*)'),
            body=callback_mock,
        )
        # Prepare valid token in client's session
        self.transport._session.headers[Transport.AUTH_HEADER] = 'valid_token'
        body = self.transport._authorized_request(
            'post', 'category/asdListResource'
        )
        assert body == ['asd']
        assert callback_mock.call_count == 1

    def test_no_token(self):
        """Get resource without token.

        First request after client initialization.
        """
        callback_mock = Mock(side_effect=self.token_logic)
        httpretty.register_uri(
            method=httpretty.POST,
            uri=re.compile(BASE_URL + '(.*)'),
            body=callback_mock,
        )
        body = self.transport._authorized_request(
            'post', 'category/asdListResource'
        )
        assert body == ['asd']
        assert callback_mock.call_count == 2

    def test_expired_token(self):
        """Get resource with expired token.

        To get data with expired token 3 requests will be made:
        1. Get resource. Response will tell "token has expired",
        2. Refresh token (login),
        3. Get resource again that returns expected data.
        """
        callback_mock = Mock(side_effect=self.token_logic)
        httpretty.register_uri(
            method=httpretty.POST,
            uri=re.compile(BASE_URL + '(.*)'),
            body=callback_mock,
        )
        # Prepare expired token in client's session
        self.transport._session.headers[Transport.AUTH_HEADER] = (
            'expired_token'
        )
        body = self.transport._authorized_request(
            'post', 'category/asdListResource'
        )
        assert body == ['asd']
        assert callback_mock.call_count == 3
