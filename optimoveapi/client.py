from .api import (
    Actions,
    Customers,
    General,
)
from .transport import Transport


class Optimove(object):

    def __init__(self, base_url, username, password):
        transport = Transport(base_url, username, password)
        self.actions = Actions(transport)
        self.customers = Customers(transport)
        self.general = General(transport)
