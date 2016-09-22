import json

import httpretty

from ..constants import BASE_URL
from ..utils import ApiCategoryTestCase


class IntegrationsTests(ApiCategoryTestCase):

    TEST_PROMOTIONS = [{
        'PromoCode': '123',
        'PromotionName': 'PURPLE_PROMO_2'
    }, {
        'PromoCode': '456',
        'PromotionName': 'PROMO_VIA_API_2'
    }]

    def test_add_promotions(self):
        promotions = {123: 'TEST'}
        httpretty.register_uri(
            httpretty.POST,
            BASE_URL + '/integrations/AddPromotions',
            body=''
        )
        body = self.optimove.integrations.add_promotions(promotions)
        request = httpretty.last_request()
        assert body is None
        assert request.body == (
            '[{"PromotionName": "TEST", "PromoCode": 123}]'
        )

    def test_get_promotions(self):
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/integrations/GetPromotions',
            body=json.dumps(self.TEST_PROMOTIONS),
        )
        body = self.optimove.integrations.get_promotions()
        assert body == self.TEST_PROMOTIONS

    def test_delete_promotions(self):
        codes = [123]
        httpretty.register_uri(
            httpretty.POST,
            BASE_URL + '/integrations/DeletePromotions',
            body='',
        )
        body = self.optimove.integrations.delete_promotions(codes)
        request = httpretty.last_request()
        assert body is None
        assert request.body == '[{"PromoCode": 123}]'
