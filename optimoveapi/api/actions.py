import logging

from ..utils import date_to_str


logger = logging.getLogger(__name__)


class Actions(object):
    """Namespace class for action-related endpoints"""

    def __init__(self, transport):
        self._transport = transport

    def get_executed_campaign_details(self, date):
        logger.info('Getting executed campaign for %s', date)
        path = 'actions/GetExecutedCampaignDetails'
        params = {
            'Date': date_to_str(date),
        }
        executed_campaign_details = self._transport.get(path, params)
        logger.info('Got %s executed campaign', len(executed_campaign_details))
        return executed_campaign_details

    def get_promo_codes_by_campaign(self, campaign_id):
        logger.info('Getting promo codes for campaign %s', campaign_id)
        path = 'actions/GetPromoCodesByCampaign'
        params = {
            'CampaignID': campaign_id,
        }
        promo_codes_by_campaign = self._transport.get(path, params)
        logger.info('Got %s promo codes', len(promo_codes_by_campaign))
        return promo_codes_by_campaign

    def get_promo_codes_by_target_group(self, target_group_id, date):
        path = 'actions/GetPromoCodesByTargetGroup'
        params = {
            'TargetGroupID': target_group_id,
            'Date': date_to_str(date),
        }
        return self._transport.get(path, params)
