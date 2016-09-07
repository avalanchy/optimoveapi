from ..utils import str_to_date


class General(object):

    def __init__(self, transport):
        self._transport = transport

    def get_last_data_update(self):
        path = 'general/GetLastDataUpdate'
        body = self._transport.get(path)
        body['Date'] = str_to_date(body['Date'])
        return body
