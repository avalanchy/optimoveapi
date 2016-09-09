from ..utils import date_to_str


class Actions(object):

    def __init__(self, transport):
        self._transport = transport

    def get_executed_campaign_details(self, date):
        path = 'actions/GetExecutedCampaignDetails'
        params = {
            'Date': date_to_str(date),
        }
        return self._transport.get(path, params)

    def get_promo_codes_by_campaign(self, campaign_id):
        path = 'actions/GetPromoCodesByCampaign'
        params = {
            'CampaignID': campaign_id,
        }
        return self._transport.get(path, params)

    def get_promo_codes_by_target_group(self, target_group_id, date):
        path = 'actions/GetPromoCodesByTargetGroup'
        params = {
            'TargetGroupID': target_group_id,
            'Date': date_to_str(date),
        }
        return self._transport.get(path, params)
