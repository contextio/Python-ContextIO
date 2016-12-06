from __future__ import absolute_import
import logging

from .base_resource import BaseResource

class Discovery(BaseResource):
    """Class to represent the Discovery resource.

    Properties:
        email: string - The email address requested for discovery
        found: bool - true if settings were found, false otherwise
        type: string - Type of provider, (eg. "gmail")
        imap: dict - information about the imap server, data format below
            "imap": {
                "server": string - FQDN of the IMAP server,
                "username": string - What the username should be for
                    authentication,
                "port": number - Network port IMAP server is listening on,
                "use_ssl": boolean - Whether that server:port uses SSL
                    encrypted connections,
                "oauth": boolean - true if the IMAP server support
                    authentication through OAuth (setting related OAuth
                    consumers)
              }
        documentation: list - List of documentation pages that may be useful
            for end-users for this specific IMAP provider
    """

    keys = ['email', 'found', 'type', 'imap', 'documentation']

    def __init__(self, parent, defn):
        """Constructor.

        Required Arguments:
            parent: ContextIO object - parent is an ContextIO object.
            defn: a dictionary of parameters.
        """
        super(Discovery, self).__init__(parent, 'discovery', defn)

    def get(self):
        logging.info("This method is not implemented")

    def put(self):
        logging.info("This method is not implemented")

    def post(self):
        logging.info("This method is not implemented")

    def delete(self):
        logging.info("This method is not implemented")
