from ..constants import DATE_FORMAT


class Action(object):

    def __init__(self, transport):
        self._transport = transport

    def get_executed_campaign_details(self, date):
        path = 'actions/GetExecutedCampaignDetails'
        date_str = date.strftime(DATE_FORMAT)
        params = {
            'Date': date_str,
        }
        return self._transport.get(path, params)
