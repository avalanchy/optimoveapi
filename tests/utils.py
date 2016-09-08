from unittest import TestCase

import httpretty

from optimoveapi import Optimove
from .constants import BASE_URL


class ApiCategoryTestCase(TestCase):
    """Base class for testing Optimove's category specific endpoints"""

    @classmethod
    def setUpClass(cls):
        # Enabling HTTPretty via `activate` decorator does not allow to mock
        # URI in setUp or setUpClass, so I am doing this via enable()/disable()
        httpretty.enable()
        # Mock login URI for every test
        httpretty.register_uri(
            httpretty.POST,
            BASE_URL + '/general/login',
            body='"token"',
            content_type='application/json',
        )
        # Share instantiated client
        cls.optimove = Optimove(BASE_URL, 'username', 'password')

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()
