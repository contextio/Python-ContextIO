from __future__ import absolute_import

import logging

from .. import helpers
from .base_resource import BaseResource
from .connect_token import ConnectToken
from .folder import Folder

class Source(BaseResource):
    """Class to represent the Source resource.

    Properties:
        username: string - The username used to authenticate an IMAP connection.
            On some servers, this is the same thing as the primary email
            address.
        status: string - If the status of the source is TEMP_DISABLED or
            DISABLED. You can do a POST/PUT with status set to 1 to reset it.
        type: string - Currently, the only supported type is IMAP
        label: string - The label property of the source instance. You can use
            0 as an alias for the first source of an account.
        use_ssl: integer - Set to 1 if you want SSL encryption to be used when
            opening connections to the IMAP server. Any other value will be
            considered as "do not use SSL"
        resource_url: string (url) - Complete url of the source.
        server: string - Name of IP of the IMAP server, eg. imap.gmail.com
        port: integer - Port number to connect to on the server. Keep in mind
            that most IMAP servers will have one port for standard connection
            and another one for encrypted connection (see use-ssl parameter
            above)
    """
    resource_id = "label"
    keys = ["username", "status", "type", "label", "use_ssl", "resource_url", "server", "port"]

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: Account object - parent is an Account object.
            definition: a dictionary of parameters. The 'label' parameter is
                required to make method calls.
        """

        super(Source, self).__init__(parent, "sources/{label}",  definition)

    def get(self):
        """Get parameters and status for an IMAP source.

        Documentation: http://context.io/docs/2.0/accounts/sources#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        return super(Source, self).get()

    def put(self):
        logging.info("This method is not implemented")

    def delete(self):
        """Delete a data source for an account.

        Documentation: http://context.io/docs/2.0/accounts/sources#id-delete

        Arguments:
            None

        Returns:
            Bool
        """
        return super(Source, self).delete()

    def post(self, **params):
        """Update a data source for an account.

        Documentation: http://context.io/docs/2.0/accounts/sources#id-post

        Optional Arguments:
            status: integer - If the status of the source is TEMP_DISABLED or
                DISABLED. You can do a POST/PUT with status set to 1 to reset
                it.
            force_status_check: integer - Creates an IMAP connection and
                resets the source status to to one reported by the IMAP
                backend. Don't combine this with other parameters.
            sync_all_folders: integer - By default, we filter out some folders
                like 'Deleted Items' and 'Drafts'. Set this parameter to 1 to
                turn off this filtering and show every single folder.
            expunge_on_deleted_flag: integer - By default, we don't filter out
                messages flagged as deleted. Set this parameter to 1 to turn on
                this filtering.
            password: string - New password for this source. Ignored if any of
                the provider_* parameters are set below.
            provider_refresh_token: An OAuth2 refresh token obtained from the IMAP
                account provider to authenticate this email account.
            provider_consumer_key: string - The OAuth consumer key used to
                obtain the the token and token secret above for that account.
                That consumer key and secret must be configured in your
                Context.IO account
            status_callback_url: string - If specified, we'll make a POST request
                to this URL if the connection status of the source changes.

        Returns:
            Bool
        """
        all_args = ['status', 'force_status_check', 'sync_all_folders',
            'expunge_on_deleted_flag', 'password', 'provider_refresh_token',
            'provider_consumer_key', 'status_callback_url'
        ]

        return super(Source, self).post(params=params, all_args=all_args)

    def delete_connect_token(self, token_id):
        """Removes a connect token created for an IMAP source.

        Documentation: http://context.io/docs/2.0/accounts/sources/connect_tokens#delete

        Arguments: None

        Returns:
            A single ConnectToken object
        """

        return self._request_uri("connect_tokens/{0}".format(token_id), method="DELETE")

    def get_connect_token(self, token_id):
        """Retrieve a single connect token created for an IMAP source.

        Documentation: http://context.io/docs/2.0/accounts/sources/connect_tokens#get

        Arguments: None

        Returns:
            A single ConnectToken object
        """

        return ConnectToken(self, self._request_uri("connect_tokens/{0}".format(token_id)))

    def get_connect_tokens(self):
        """List of connect tokens created for an IMAP source.

        Documentation: http://context.io/docs/2.0/accounts/sources/connect_tokens#get

        Arguments: None

        Returns:
            A list of ConnectToken objects
        """
        return [ConnectToken(self, obj) for obj in self._request_uri('connect_tokens')]

    def post_connect_token(self, **params):
        """Obtain a new connect_token for an IMAP source.

        * Note: unused connect tokens are purged after 24 hours.

        Documentation: http://context.io/docs/2.0/accounts/sources/connect_tokens#post

        Required Arguments:
            callback_url: string (url) - When the user's mailbox is connected
                to your API key, the browser will call this url (GET). This
                call will have a parameter called contextio_token indicating
                the connect_token related to this callback. You can then do a
                get on this connect_token to obtain details about the account
                and source created through that token and save that account id
                in your own user data.

        Returns:
            A dictionary (data format below)

            {
              "success": string - true if connect_token was successfully
                  created, false otherwise,
              "token": string - Id of the token,
              "resource_url": string - URL to of the token,
              "browser_redirect_url": string - Redirect the user's browser to
                  this URL to have them connect their mailbox through this
                  token
            }
        """
        all_args = req_args = ['callback_url']

        params = helpers.sanitize_params(params, all_args, req_args)

        return self._request_uri('connect_tokens', method='POST', params=params)

    def get_folders(self, **params):
        """Get list of folders in an IMAP source.

        Documentation: http://context.io/docs/2.0/accounts/sources/folders#get

        Optional Arguments:
            include_extended_counts: integer -

        Returns:
            A list of Folder objects.
        """
        all_args = ["include_extended_counts"]
        params = helpers.sanitize_params(params, all_args)

        return [Folder(self, obj) for obj in self._request_uri("folders", params=params)]

    def get_sync(self):
        """Get sync status of a data source.

        Documentation: http://context.io/docs/2.0/accounts/sources/sync#get

        Arguments:
            None

        Returns:
            A dictionary, data format below

            {
                'Source.label': {
                    'last_sync_start': UNIX TIME STAMP (int),
                    'last_sync_stop': UNIX TIME STAMP (int),
                    'last_expunge': UNIX TIME STAMP (int),
                    'initial_import_finished': BOOL
                }
            }
        """
        return self._request_uri("sync")

    def post_sync(self):
        """Trigger a sync of a data source.

        Documentation: http://context.io/docs/2.0/accounts/sources/sync#post

        Arguments:
            None

        Returns
            a dictionary, data format below

            {
                'syncs_queued': LIST of syncs queued,
                'resource_url': STRING, complete url of resource,
                'success': BOOL,
                'label': STRING, source label
            }
        """
        return self._request_uri('sync', method='POST')
