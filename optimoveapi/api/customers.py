from ..utils import date_to_str


class Customers(object):

    MAX_PAGE_LENGTH = 10000

    def __init__(self, transport):
        self._transport = transport

    def _get_all_pages(self, path, params):
        """ Returns all pages merged.

        All customer-related endpoints return a maximum of 10,000 records
        per page. To get all pages `$skip` parameter need to be used.
        """
        merged_pages = []
        skip = 0
        while 1:
            params['$skip'] = skip
            body = self._transport.get(path, params)
            merged_pages.extend(body)
            if len(body) < self.MAX_PAGE_LENGTH:
                break
            skip += self.MAX_PAGE_LENGTH
        return merged_pages

    def get_customer_actions_by_target_group(self, target_group_id, date):
        path = 'customers/GetCustomerActionsByTargetGroup'
        params = {
            'TargetGroupID': target_group_id,
            'Date': date_to_str(date),
        }
        return self._get_all_pages(path, params)

    def get_customer_one_time_action_by_date(self, date):
        path = 'customers/GetCustomerOneTimeActionsByDate'
        params = {
            'Date': date_to_str(date),
        }
        return self._get_all_pages(path, params)
