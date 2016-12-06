from __future__ import absolute_import

from requests.exceptions import HTTPError

class ArgumentError(Exception):
    """Class to handle bad arguments."""
    pass

class MissingResourceId(Exception):
    """Class to handle missing required argument on resource init."""
    pass

class RequestError(HTTPError):
    pass
