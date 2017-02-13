from __future__ import absolute_import

from .api import Api
from .helpers import sanitize_params
from .resources.account import Account
from .resources.webhook import WebHook


class V2_0(Api):
    def get_accounts(self, **params):
        """List of Accounts.

        GET method for the accounts resource.

        Documentation: http://context.io/docs/2.0/accounts#get

        Optional Arguments:
            email: string - Only return account associated
                to this email address
            status: string - Only return accounts with sources
                whose status is of a specific value. If an account has many
                sources, only those matching the given value will be
                included in the response. Possible statuses are:
                INVALID_CREDENTIALS, CONNECTION_IMPOSSIBLE,
                NO_ACCESS_TO_ALL_MAIL, OK, TEMP_DISABLED and DISABLED
            status_ok: int - Only return accounts with sources
                whose status is of a specific value. If an account has many
                sources, only those matching the given value will be included
                in the response. Possible statuses are: INVALID_CREDENTIALS,
                CONNECTION_IMPOSSIBLE, NO_ACCESS_TO_ALL_MAIL, OK, TEMP_DISABLED
                and DISABLED
            limit: int - The maximum number of results to return
            offset: int - Start the list at this offset (zero-based)

        Returns:
            A list of Account objects
        """
        all_args = ["email", "status", "status_ok", "limit", "offset"]

        params = sanitize_params(params, all_args)
        return [Account(self, obj) for obj in self._request_uri("accounts", params=params)]

    def post_account(self, **params):
        """Add a new account.

        POST method for the accounts resource.

        You can optionally pass in the params to simultaneously add a source
        with just this one call. In order to accomplish this you must include all of the
        required parameters to create a source AS WELL AS one of the following:
            - the password for the source
            - the provider_refresh_token AND provider_consumer_key

            *see https://context.io/docs/2.0/accounts/sources#post for more information*

        Documentation: http://context.io/docs/2.0/accounts#post

        Required Arguments:
            email: string - The primary email address of the account holder.
            migrate_account_id: string - Existing user_id (from lite) you want
               to migrate to 2.0. Either migrate_account_id or email must be specified

        Optional Arguments:
            first_name: string - First name of the account holder.
            last_name: string - Last name of the account holder.

        If adding a source in the same call:
        Required Arguments:
            server: string - Name or IP of the IMAP server, eg. imap.gmail.com
            username: string - The username used to authenticate an IMAP
                connection. On some servers, this is the same thing as
                the primary email address.
            use_ssl: integer - Set to 1 if you want SSL encryption to
                be used when opening connections to the IMAP server. Any
                other value will be considered as "do not use SSL"
            port: integer - Port number to connect to on the server. Keep in
                mind that most IMAP servers will have one port for standard
                connection and another one for encrypted connection (see
                use-ssl parameter above)
            type: string - Currently, the only supported type is IMAP

        Optional Arguments:
            origin_ip: string - IP address of the end user requesting the account
                to be created
            expunge_on_deleted_flag: integer - By default, we don't filter out messages
                flagged as deleted. Set this parameter to 1 to turn on this filtering.
            sync_all_folders: integer - By default, we filter out some folders like
                'Deleted Items' and 'Drafts'. Set this parameter to 1 to turn off this
                filtering and show every single folder.
            sync_folders: string - By default, we filter out some folders like
                'Deleted Items' and 'Drafts'. Set this parameter to
                'All,Trash' to show the 'Deleted Items' folder.
            sync_flags:  integer By default, we don't synchronize IMAP flags.
                Set this parameter to 1 to turn on IMAP flag syncing for the 'seen' and
                'flagged' flags.
            raw_file_list: integer - By default, we filter out files like
                signature images or those winmail.dat files form the files
                list. Set this parameter to 1 to turn off this filtering and
                show every single file attachments.
            password: string - Password for authentication on the IMAP server.
                Ignored if any of the provider_* parameters are set below.
            provider_refresh_token: An OAuth2 refresh token obtained from the
                IMAP account provider to be used to authenticate on this email
                account.
            provider_consumer_key: string - The OAuth consumer key used to
                obtain the the token and token secret above for that account.
                That consumer key and secret must be configured in your
                Context.IO account.
            callback_url: string (url) - If specified, we'll make a POST
                request to this URL when the initial sync is completed.
                status_callback_url: string (url) - If specified, we'll make a POST
                request to this URL if the connection status of the source changes.

        Returns:
            An Account object
        """
        req_args = ["email"]
        all_args = ["email", "migrate_account_id", "first_name", "last_name", "server",
            "username", "use_ssl", "port", "type", "origin_ip", "expunge_on_deleted_flag",
            "sync_all_folders", "sync_folders", "sync_flags", "raw_file_list", "password",
            "provider_refresh_token", "provider_consumer_key", "callback_url", "status_callback_url"
        ]

        params = sanitize_params(params, all_args, req_args)

        return Account(self, self._request_uri("accounts", method="POST", params=params))

    def post_connect_token(self, **params):
        """Obtain a new connect token.

        2.0
        Documentation: http://context.io/docs/2.0/connect_tokens#post

        Lite
        Documentation: http://context.io/docs/lite/connect_tokens#post

        Required Arguments:
            callback_url: string (url) - When the user's mailbox is connected
                to your API key, the browser will call this url (GET). This
                call will have a parameter called contextio_token indicating
                the connect_token related to this callback. You can then do a
                get on this connect_token to obtain details about the account
                and source created through that token and save that account id
                in your own user data.

        Optional Arguments:
            email: string - The email address of the account to be added. If
                specified, the first step of the connect UI where users are
                prompted for their email address, first name and last name is
                skipped.
            first_name: string - First name of the account holder.
            last_name: string - Last name of the account holder.
            source_callback_url: string - If specified, we'll make a POST
                request to this URL when the initial sync is completed.
            source_sync_all_folders: integer - By default, we filter out some
                folders like 'Deleted Items' and 'Drafts'. Set this parameter
                to 1 to turn off this filtering and show every single folder.
            source_sync_flags: integer - By default, we don't synchronize IMAP
                flags. Set this parameter to 1 to turn on IMAP flag syncing
                for the 'seen' and 'flagged' flags.
            source_raw_file_list: integer - By default, we filter out files
                like signature images from the files list. Set this parameter
                to 1 to turn off this filtering and show every single file
                attachment.
            status_callback_url: string (url) - If specified, we'll make a POST
            request to this URL if the connection status of the source changes.

        Returns:
            A dictionary, data format below

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
        req_args = ["callback_url"]
        all_args = [
            "callback_url", "email", "first_name", "last_name",
            "source_callback_url", "source_sync_all_folders",
            "source_sync_flags", "source_raw_file_list", "status_callback_url"
        ]

        params = sanitize_params(params, all_args, req_args)
        return super(V2_0, self).post_connect_token(**params)

    def get_webhooks(self):
        return [WebHook(self, obj) for obj in self._request_uri("webhooks")]

    def post_webhook(self, **params):
        req_args = ["callback_url", "failure_notif_url"]
        all_args = ["callback_url", "failure_notif_url", "filter_to", "filter_from", "filter_cc",
            "filter_subject", "filter_thread", "filter_new_important",
            "filter_file_name", "filter_folder_added", "filter_folder_removed",
            "filter_to_domain", "filter_from_domain"
        ]

        params = sanitize_params(params, all_args, req_args)

        return self._request_uri("webhooks", method="POST", params=params)
