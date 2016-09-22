from unittest import TestCase

import httpretty

from optimoveapi import Optimove
from .constants import BASE_URL


class ApiCategoryTestCase(TestCase):
    """Base class for testing Optimove's category specific endpoints.

    Enables HTTPretty and mocks login URI for every test.
    """

    def setUp(self):
        # HTTPretty offers initializing it's socket's monkey-patching trough
        # `activate` decorator. But it does not work setUp method, so I am
        # doing this manually using `reset/enable/disable`.
        httpretty.reset()
        httpretty.enable()
        # Mock login URI for every test
        httpretty.register_uri(
            httpretty.POST,
            BASE_URL + '/general/login',
            body='"valid_token"',
            content_type='application/json',
        )
        # Share instantiated client
        self.optimove = Optimove(BASE_URL, 'username', 'password')

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()
