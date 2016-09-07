import logging

import requests

from .exceptions import (
    ExpiredToken,
    OptimoveError,
)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Transport(object):

    AUTH_HEADER = 'Authorization-Token'

    def __init__(self, base_url, username, password):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._session = requests.Session()

    def get(self, path, data=None):
        return self._authorized_request('get', path, params=data)

    def post(self, path, data):
        return self._authorized_request('post', path, json=data)

    def _general_login(self):
        path = 'general/login'
        json = {
            'Username': self._username,
            'Password': self._password,
        }
        logger.info('Obtaining token')
        return self._request('post', path, json=json)

    def _authorized_request(self, method, path, json=None, params=None):
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
        url = '{}/{}'.format(self._base_url, path)
        try:
            response = self._session.request(
                method,
                url,
                json=json,
                params=params,
            )
        except requests.RequestException:
            logger.exception('Requests lib raised an exception')
            raise OptimoveError('Network error')
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
        try:
            body = response.json()
        except ValueError:
            logger.exception('Unable to read returned JSON')
            logger.debug('Response HTTP code: %s', response.status_code)
            logger.debug('Response raw content: %s', response.content)
            raise OptimoveError('Unable to decode returned JSON')
        return body