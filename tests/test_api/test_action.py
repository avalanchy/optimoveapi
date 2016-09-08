import datetime

import httpretty

from ..constants import BASE_URL
from ..utils import ApiCategoryTestCase


class ActionTests(ApiCategoryTestCase):

    def test_get_executed_campaign_details(self):
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/actions/GetExecutedCampaignDetails',
            body='[]',  # TODO extend with mocked result
            content_type='application/json',
        )
        date = datetime.date(2016, 9, 6)
        body = self.optimove.action.get_executed_campaign_details(date)
        assert body == []
