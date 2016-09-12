import datetime
import json

import httpretty

from ..constants import BASE_URL
from ..utils import ApiCategoryTestCase


class CustomersTests(ApiCategoryTestCase):

    CUSTOMERS = [
        {
            'CustomerID': '1000926',
            'ActionID': 62,
            'ChannelID': 15
        }, {
            'CustomerID': '1008451',
            'ActionID': 62,
            'ChannelID': 15
        },
    ]

    def test_get_customer_actions_by_target_group(self):
        customers = self.CUSTOMERS
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/customers/GetCustomerActionsByTargetGroup',
            body=json.dumps(customers),
            content_type='application/json',
        )
        body = self.optimove.customers.get_customer_actions_by_target_group(
            123,
            datetime.date(2016, 9, 12),
        )
        assert body == customers

    def test_get_customer_one_time_action_by_date(self):
        customers = self.CUSTOMERS
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/customers/GetCustomerOneTimeActionsByDate',
            body=json.dumps(customers),
            content_type='application/json',
        )
        body = self.optimove.customers.get_customer_one_time_action_by_date(
            datetime.date(2016, 9, 12),
        )
        assert body == customers
