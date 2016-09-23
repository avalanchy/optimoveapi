import logging

from ..utils import str_to_date


logger = logging.getLogger(__name__)


class General(object):
    """Namespace class for general endpoints"""

    def __init__(self, transport):
        self._transport = transport

    def get_last_data_update(self):
        logger.info('Getting last data update')
        path = 'general/GetLastDataUpdate'
        body = self._transport.get(path)
        last_data_update = str_to_date(body['Date'])
        logger.info('Got date %s', last_data_update)
        return last_data_update
