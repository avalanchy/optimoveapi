from .api import (
    Action,
    General,
)
from .transport import Transport


class Optimove(object):

    def __init__(self, base_url, username, password):
        transport = Transport(base_url, username, password)
        self.action = Action(transport)
        self.general = General(transport)
