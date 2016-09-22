import datetime
import json

from mock import (
    Mock,
    patch,
)
import httpretty

from optimoveapi.api import Customers

from ..constants import BASE_URL
from ..utils import ApiCategoryTestCase


class CustomersTests(ApiCategoryTestCase):
    TEST_PAGE_LENGTH = 2
    TEST_CUSTOMER = [
        {
            'CustomerID': '1000926',
            'ActionID': 62,
            'ChannelID': 15
        },
    ]

    def pagination_logic(self, items_count):
        """Simulates Optimove's logic around pagination"""
        customers = self.TEST_CUSTOMER * items_count

        def call(request, _, headers):
            skip = int(request.querystring['$skip'][0])
            body = customers[skip:skip+self.TEST_PAGE_LENGTH]
            return 200, headers, json.dumps(body)

        return call

    @patch.object(Customers, 'MAX_PAGE_LENGTH', TEST_PAGE_LENGTH)
    def test_get_1_page_with_extra_call_to_see_if_there_is_more(self):
        callback_mock = Mock(side_effect=self.pagination_logic(2))
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/customers/ThisIsFakeTestURI',
            body=callback_mock,
        )
        body = self.optimove.customers._get_all_pages(
            'customers/ThisIsFakeTestURI',
            {'asd': 123}
        )
        assert len(body) == 2
        assert callback_mock.call_count == 2

    @patch.object(Customers, 'MAX_PAGE_LENGTH', TEST_PAGE_LENGTH)
    def test_get_all_3_pages(self):
        callback_mock = Mock(side_effect=self.pagination_logic(5))
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/customers/ThisIsFakeTestURI',
            body=callback_mock,
        )
        body = self.optimove.customers._get_all_pages(
            'customers/ThisIsFakeTestURI',
            {'asd': 123}
        )
        assert len(body) == 5
        assert callback_mock.call_count == 3

    def test_get_customer_actions_by_target_group(self):
        customers = self.TEST_CUSTOMER * 2
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/customers/GetCustomerActionsByTargetGroup',
            body=json.dumps(customers),
        )
        body = self.optimove.customers.get_customer_actions_by_target_group(
            123,
            datetime.date(2016, 9, 12),
        )
        assert body == customers

    def test_get_customer_one_time_action_by_date(self):
        customers = self.TEST_CUSTOMER * 2
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/customers/GetCustomerOneTimeActionsByDate',
            body=json.dumps(customers),
        )
        body = self.optimove.customers.get_customer_one_time_action_by_date(
            datetime.date(2016, 9, 12),
        )
        assert body == customers

    def test_get_customers_by_action(self):
        customers = self.TEST_CUSTOMER * 2
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/customers/GetCustomersByAction',
            body=json.dumps(customers),
            content_type='application/json',
        )
        body = self.optimove.customers.get_customers_by_action(
            datetime.date(2016, 9, 12), 1, 2,
        )
        assert body == customers
