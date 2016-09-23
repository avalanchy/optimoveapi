import logging

from simplejson import JSONDecodeError
import requests

from .exceptions import (
    ExpiredToken,
    OptimoveError,
)


logger = logging.getLogger(__name__)


class Transport(object):
    """Network communication with Optimove.

    Keep single session, transparently handles authorization, covers errors.
    Utilizes requests library.
    """

    AUTH_HEADER = 'Authorization-Token'

    def __init__(self, base_url, username, password):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._session = requests.Session()
        # This won't retry requests where data has made it way to the server
        adapter = requests.sessions.HTTPAdapter(max_retries=2)
        self._session.mount('https://', adapter)

    def get(self, path, data=None):
        """Public method for GET-based endpoints"""
        return self._authorized_request('get', path, params=data)

    def post(self, path, data):
        """Public method for POST-based endpoints"""
        return self._authorized_request('post', path, json=data)

    def _general_login(self):
        """Method for obtaining authorization token by sending credentials.

        Uses POST which is marginally more secure.
        """
        path = 'general/login'
        json = {
            'Username': self._username,
            'Password': self._password,
        }
        logger.info('Obtaining token')
        return self._request('post', path, json=json)

    def _authorized_request(self, method, path, json=None, params=None):
        """Transparently covers logic for Optimove's token-based authorization.

        Request the token and sets it as a header. Repeats if token is expired.
        """
        if self.AUTH_HEADER not in self._session.headers:
            logger.info('No token')
            self._session.headers[self.AUTH_HEADER] = self._general_login()
        try:
            return self._request(method, path, json, params)
        except ExpiredToken:
            logger.info('Token has expired')
            self._session.headers[self.AUTH_HEADER] = self._general_login()
            return self._request(method, path, json, params)

    def _request(self, method, path, json=None, params=None):
        """Lowest level code in scope of client that do request to Optimove.

        Checks if something went wrong and if so - trows an OptimoveError
        (or child) otherwise returns decoded json.
        """
        url = '{}/{}'.format(self._base_url, path)
        try:
            response = self._session.request(
                method,
                url,
                json=json,
                params=params,
            )
        except requests.RequestException as e:
            logger.exception('Requests lib raised an exception')
            raise OptimoveError(str(e))
        is_token_expired = (
            response.status_code == ExpiredToken.CODE and
            response.text == ExpiredToken.MESSAGE
        )
        if is_token_expired:
            raise ExpiredToken
        if response.status_code != 200:
            logger.error('Optimove returned unexpected status code')
            logger.debug('Response HTTP code: %s', response.status_code)
            logger.debug('Response raw content: %s', response.content)
            raise OptimoveError('Unexpected returned code')
        if response.headers['Content-Length'] == '0':
            return None
        try:
            body = response.json()
        except JSONDecodeError:
            logger.exception('Unable to read returned JSON')
            logger.debug('Response HTTP code: %s', response.status_code)
            logger.debug('Response raw content: %s', response.content)
            raise OptimoveError('Unable to decode returned JSON')
        return body
