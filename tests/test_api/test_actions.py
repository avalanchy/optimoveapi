import datetime
import json

import httpretty

from ..constants import BASE_URL
from ..utils import ApiCategoryTestCase


class ActionsTests(ApiCategoryTestCase):

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
        )
        date = datetime.date(2016, 9, 5)
        body = self.optimove.actions.get_executed_campaign_details(date)
        assert body == executed_campaigns

    def test_get_promo_codes_by_campaign(self):
        promo_codes = [
            {
              "RecipientGroupID": 1,
              "ActionID": 85,
              "PromoCode": ""
            }
        ]
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/actions/GetPromoCodesByCampaign',
            body=json.dumps(promo_codes),
        )
        body = self.optimove.actions.get_promo_codes_by_campaign(123)
        assert body == promo_codes

    def test_get_promo_codes_by_target_group(self):
        promo_codes = [
            {
                'RecipientGroupID': 1,
                'ActionID': 24,
                'PromoCode': 'HEP-FEB'
            }, {
                'RecipientGroupID': 2,
                'ActionID': 25,
                'PromoCode': 'HEP-FCC'
            }, {
                'RecipientGroupID': 1,
                'ActionID': 65,
                'PromoCode': 'GDG-FAL'
            }
        ]
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/actions/GetPromoCodesByTargetGroup',
            body=json.dumps(promo_codes),
        )
        date = datetime.date(2016, 9, 5)
        body = self.optimove.actions.get_promo_codes_by_target_group(1, date)
        assert body == promo_codes
