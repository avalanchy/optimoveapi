class OptimoveError(Exception):
    """Raised when request to API ends with some kind of error"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.message


class ExpiredToken(OptimoveError):
    """Raised when Optimove responses with  that token is expired"""

    CODE = 403
    MESSAGE = 'Authorization-Token Expired'

    def __init__(self):
        pass

    def __unicode__(self):
        return self.MESSAGE
