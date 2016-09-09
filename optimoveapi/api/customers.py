from ..utils import date_to_str


class Customers(object):

    def __init__(self, transport):
        self._transport = transport

    def get_customer_actions_by_target_group(self, target_group_id, date):
        path = 'customers/GetCustomerActionsByTargetGroup'
        params = {
            'TargetGroupID': target_group_id,
            'Date': date_to_str(date),
        }
        return self._transport.get(path, params)

    def get_customer_one_time_action_by_date(self, date):
        path = 'customers/GetCustomerOneTimeActionsByDate'
        params = {
            'Date': date_to_str(date),
        }
        return self._transport.get(path, params)
