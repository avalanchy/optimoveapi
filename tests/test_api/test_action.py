import datetime
import json

import httpretty

from ..constants import BASE_URL
from ..utils import ApiCategoryTestCase


class ActionTests(ApiCategoryTestCase):

    def test_get_executed_campaign_details(self):
        executed_campaigns = [
            {
                'CampaignID': 1,
                'CampaignType': 'Test/Control',
                'Duration': 1,
                'Error': '',
                'IsMultiChannel': True,
                'IsRecurrence': False,
                'LeadTime': 0,
                'Notes': '',
                'Status': 'Successful',
                'TargetGroupID': 61
            }, {
                'CampaignID': 2,
                'CampaignType': 'Test/Control',
                'Duration': 1,
                'Error': '',
                'IsMultiChannel': False,
                'IsRecurrence': True,
                'LeadTime': 0,
                'Notes': '',
                'Status': 'Successful',
                'TargetGroupID': 62
            }
        ]
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/actions/GetExecutedCampaignDetails',
            body=json.dumps(executed_campaigns),
            content_type='application/json',
        )
        date = datetime.date(2016, 9, 5)
        body = self.optimove.action.get_executed_campaign_details(date)
        assert body == executed_campaigns

    def test_get_promo_codes_by_target_group(self):
        promo_codes = []  # TODO fill this with API dump
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/actions/GetPromoCodesByTargetGroup',
            body=json.dumps(promo_codes),
            content_type='application/json',
        )
        date = datetime.date(2016, 9, 5)
        body = self.optimove.action.get_promo_codes_by_target_group(1, date)
        assert body == promo_codes
