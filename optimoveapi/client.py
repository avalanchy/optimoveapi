from .api import (
    Actions,
    Customers,
    General,
    Integrations,
)
from .transport import Transport


class Optimove(object):
    """The only truth class for python-level Optimove communication.

    Initializes transport layer and shares it's instance with all
    endpoints categories.
    """

    def __init__(self, base_url, username, password):
        transport = Transport(base_url, username, password)
        self.actions = Actions(transport)
        self.customers = Customers(transport)
        self.general = General(transport)
        self.integrations = Integrations(transport)
