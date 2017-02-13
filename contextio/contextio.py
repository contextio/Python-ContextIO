from __future__ import absolute_import

from .lib.v2_0 import V2_0
from .lib.lite import Lite


def ContextIO(consumer_key, consumer_secret, **kwargs):
    if kwargs.get("api_version") == "lite":
        return Lite(consumer_key, consumer_secret, **kwargs)
    else:
        return V2_0(consumer_key, consumer_secret, **kwargs)
