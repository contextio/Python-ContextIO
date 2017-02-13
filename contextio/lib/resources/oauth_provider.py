from __future__ import absolute_import
import logging

from .base_resource import BaseResource

class OauthProvider(BaseResource):
    """Class representation of the OauthProvider resource.

    Properties:
        type: string - Identification of the OAuth provider. This must be
            either GMAIL and GOOGLEAPPSMARKETPLACE.
        provider_consumer_key: string - The OAuth consumer key
        provider_consumer_secret: string - The OAuth consumer secret
        resource_url: string - full url of the resource
    """
    resource_id = "provider_consumer_key"
    keys = ["type", "provider_consumer_key", "provider_consumer_secret",
        "resource_url"
    ]
    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: ContextIO object - parent is an ContextIO object.
            definition: a dictionary of parameters. The "provider_consumer_key"
                parameter is required to make method calls.
        """
        super(OauthProvider, self).__init__(
            parent, "oauth_providers/{provider_consumer_key}", definition)

    def get(self):
        """Get information about a given oauth provider.

        Documentation: http://context.io/docs/2.0/oauth_providers#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        return super(OauthProvider, self).get(self.parent)

    def put(self):
        logging.info("This method is not implemented")

    def post(self):
        logging.info("This method is not implemented")

    def delete(self):
        """Remove a given oauth provider.

        Documentation: http://context.io/docs/2.0/oauth_providers#id-delete

        Arguments:
            None

        Returns:
            Bool
        """
        return super(OauthProvider, self).delete()
