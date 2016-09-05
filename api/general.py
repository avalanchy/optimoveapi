import datetime

from ..constants import DATE_FORMAT


class General(object):

    def __init__(self, transport):
        self._transport = transport

    def get_last_data_update(self):
        path = 'general/GetLastDataUpdate'
        body = self._transport.get(path)
        date_str = body['Date']
        dt = datetime.datetime.strptime(date_str, DATE_FORMAT)
        return dt.date()
