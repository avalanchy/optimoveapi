import datetime

import httpretty

from ..constants import BASE_URL
from ..utils import ApiCategoryTestCase


class GeneralTests(ApiCategoryTestCase):

    def test_get_last_data_update(self):
        httpretty.register_uri(
            httpretty.GET,
            BASE_URL + '/general/GetLastDataUpdate',
            body='{"Date": "2016-09-06"}',
            content_type='application/json',
        )
        body = self.optimove.general.get_last_data_update()
        assert body == {'Date': datetime.date(2016, 9, 6)}
