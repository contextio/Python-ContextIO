from __future__ import absolute_import

import logging

from .. import helpers
from .base_resource import BaseResource
from .source import Source
from .connect_token import ConnectToken
from .contact import Contact
from .email_address import EmailAddress
from .thread import Thread
from .webhook import WebHook
from .file import File
from .message import Message


class Account(BaseResource):
    """Class to represent the Account resource.

    Properties:
        id: string - Id of the account
        username: string - Username assigned to the account
        created: integer (unix timestamp) - account creation time
        suspended: integer (unix timestamp) - account suspension time 0 means
            not suspended
        email_addresses: list - email addresses for this account
        first_name: string - First name of account holder
        last_name: string - Last name of account holder
        password_expired: integer (unix timestamp) - user's password
            expiration. 0 means still valid
        sources: list - email accounts where this account gets data from
        resource_url: string - URI which identifies this account
    """
    resource_id = "id"
    keys = [
        "id", "username", "created", "suspended", "email_addresses", "first_name", "last_name",
        "password_expired", "sources", "resource_url"
    ]

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: ContextIO object - parent is the ContextIO object to handle
                authentication.
            definition: a dictionary of parameters. The 'id' parameter is required to
                make method calls.
        """
        super(Account, self).__init__(parent, "accounts/{id}", definition)

    def get(self):
        """GET details for a given account.

        GET method for the account resource.

        Documentation: http://context.io/docs/2.0/accounts#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        return super(Account, self).get()

    def delete(self):
        """Remove a given account.

        DELETE method for the account resource.

        Documentation: http://context.io/docs/2.0/accounts#id-delete

        Arguments:
            None

        Returns:
            Bool
        """
        return super(Account, self).delete()

    def post(self, **params):
        """Modifies a given account.

        POST method for the account resource.

        Documentation: http://context.io/docs/2.0/accounts#id-post

        Optional Arguments:
            first_name: string - First name of the account holder
            last_name: string - Last name of the account holder

        Returns:
            Bool
        """

        all_args = ['first_name', 'last_name']

        for prop in all_args:
            value = params.get(prop)
            if value:
                setattr(self, prop, value)

        return super(Account, self).post(params=params, all_args=all_args)

    def put(self):
        logging.info("This method is not implemented")

    def get_connect_tokens(self):
        """List of connect tokens created for an account.

        Documentation: http://context.io/docs/2.0/accounts/connect_tokens#get

        Arguments:
            None

        Returns:
            A list of ConnectToken objects
        """

        return [ConnectToken(self, obj) for obj in self._request_uri('connect_tokens')]

    def get_contacts(self, **params):
        """List contacts in an account.

        Documentation: http://context.io/docs/2.0/accounts/contacts#get

        Optional Arguments:
            search: string - String identifying the name or the email address
                of the contact(s) you are looking for.
            active_before: integer (unix time) - Only include contacts
                included in at least one email dated before a given time. This
                parameter should be a standard unix timestamp
            active_after: integer (unix time) - Only include contacts included
                in at least one email dated after a given time. This parameter
                should be a standard unix timestamp
            sort_by: string - The field by which to sort the returned results.
                Possible values are email, count, received_count and sent_count
            sort_order: string - The sort order of the returned results.
                Possible values are asc and desc
            limit: integer - The maximum number of results to return.
            offset: integer - Start the list at this offset (zero-based).

        Returns:
            A list of Contact objects
        """
        all_args = [
            'search', 'active_before', 'active_after', 'limit', 'offset',
            'sort_by', 'sort_order'
        ]

        params = helpers.sanitize_params(params, all_args)
        contacts = self._request_uri("contacts", params=params)

        return [Contact(self, obj) for obj in contacts.get('matches')]

    def get_email_addresses(self):
        """List of email addresses used by an account.

        Documentation: http://context.io/docs/2.0/accounts/email_addresses#get

        Arguments:
            None

        Returns:
            A list of EmailAddress objects.
        """
        return [EmailAddress(self, obj) for obj in self._request_uri("email_addresses")]

    def get_files(self, **params):
        """List of files found as email attachments.

        GET method for the files resource.

        Documentation: http://context.io/docs/2.0/accounts/files

        Each of the email, to, from, cc and bcc parameters can be set to a
        comma-separated list of email addresses. These multiple addresses
        are treated as an OR combination.

        You can set more than one parameter when doing this call. Multiple
        parameters are treated as an AND combination.

        Optional Arguments:
            file_name: string - Search for files based on their name. You can
                filter names using typical shell wildcards such as *, ? and []
                or regular expressions by enclosing the search expression in a
                leading / and trailing /. For example, *.pdf would give you
                all PDF files while /\.jpe?g$/ would return all files whose
                name ends with .jpg or .jpeg
            file_size_min: integer - Search for files based on their size (in bytes).
            file_size_max: integer - Search for files based on their size (in bytes).
            email: string - Email address of the contact for whom you want the
                latest files exchanged with. By "exchanged with contact X" we
                mean any email received from contact X, sent to contact X or
                sent by anyone to both contact X and the source owner.
            to: string - Email address of a contact files have been sent to.
            from: string - Email address of a contact files have been received
                from.
            cc: string - Email address of a contact CC'ed on the messages.
            bcc: string - Email address of a contact BCC'ed on the messages.
            date_before: integer (unix time) - Only include files attached to
                messages sent before a given timestamp. The value this filter
                is applied to is the Date: header of the message which refers
                to the time the message is sent from the origin.
            date_after: integer (unix time) - Only include files attached to
                messages sent after a given timestamp. The value this filter
                is applied to is the Date: header of the message which refers
                to the time the message is sent from the origin.
            indexed_before: integer (unix time) - Only include files attached
                to messages indexed before a given timestamp. This is not the
                same as the date of the email, it is the time Context.IO
                indexed this message.
            indexed_after: integer (unix time) - Only include files attached
                to messages indexed after a given timestamp. This is not the
                same as the date of the email, it is the time Context.IO
                indexed this message.
            source: string - Filter messages by the account source label.
            sort_order: string - The sort order of the returned results.
                Possible values are asc and desc
            limit: integer - The maximum number of results to return.
            offset: integer - Start the list at this offset (zero-based).

        Returns:
            A list of File objects
        """
        all_args = [
            'file_name', 'file_size_min', 'file_size_max', 'email', 'to', 'from', 'cc', 'bcc',
            'date_before', 'date_after', 'indexed_before', 'indexed_after', 'source', 'limit',
            'offset'
        ]

        params = helpers.sanitize_params(params, all_args)

        return [File(self, obj) for obj in self._request_uri('files', params=params)]

    def get_messages(self, **params):
        """List email messages for an account.

        GET method for the messages resource.

        Each of the email, to, from, cc and bcc parameters can be set to a
        comma-separated list of email addresses. These multiple addresses
        are treated as an OR combination.

        You can set more than one parameter when doing this call. Multiple
        parameters are treated as an AND combination.

        Optional Arguments:
            subject: string - Get messages whose subject matches this search
                string. To use regular expressions instead of simple string
                matching, make sure the string starts and ends with /.
            email: string - Email address of the contact for whom you want the
                latest messages exchanged with. By "exchanged with contact X"
                we mean any email received from contact X, sent to contact X
                or sent by anyone to both contact X and the source owner.
            to: string - Email address of a contact messages have been sent to.
            sender: string - Email address of a contact messages have been
                received from. Same as "from" in documentation. "from" is a
                python keyword and we can't use that...
            cc: string - Email address of a contact CC'ed on the messages.
            bcc: string - Email address of a contact BCC'ed on the messages.
            folder: string - Filter messages by the folder (or Gmail label).
                This parameter can be the complete folder name with the
                appropriate hierarchy delimiter for the mail server being
                queried (eg. Inbox/My folder) or the "symbolic name" of the
                folder (eg. \Starred). The symbolic name refers to attributes
                used to refer to special use folders in a language-independant
                way. See http://code.google.com/apis/gmail/imap/#xlist
                (Gmail specific) and RFC-6154.
            source: string - Filter messages by the account source label.
            file_name: string - Search for files based on their name. You can
                filter names using typical shell wildcards such as *, ? and []
                or regular expressions by enclosing the search expression in a
                leading / and trailing /. For example, *.pdf would give you
                all PDF files while /\.jpe?g$/ would return all files whose
                name ends with .jpg or .jpeg
            file_size_min: integer - Search for files based on their size (in bytes).
            file_size_max: integer - Search for files based on their size (in bytes).
            date_before: integer (unix time) - Only include messages before a
                given timestamp. The value this filter is applied to is the
                Date: header of the message which refers to the time the
                message is sent from the origin.
            date_after: integer (unix time) - Only include messages after a
                given timestamp. The value this filter is applied to is the
                Date: header of the message which refers to the time the
                message is sent from the origin.
            indexed_before: integer (unix time) - Only include messages
                indexed before a given timestamp. This is not the same as the
                date of the email, it is the time Context.IO indexed this
                message.
            indexed_after: integer (unix time) - Only include messages indexed
                after a given timestamp. This is not the same as the date of
                the email, it is the time Context.IO indexed this message.
            include_thread_size: integer - Set to 1 to include thread size in the result.
            include_body: integer - Set to 1 to include message bodies in the
                result. Since message bodies must be retrieved from the IMAP
                server, expect a performance hit when setting this parameter.
            include_headers: mixed - Can be set to 0 (default), 1 or raw. If
                set to 1, complete message headers, parsed into an array, are
                included in the results. If set to raw, the headers are also
                included but as a raw unparsed string. Since full original
                headers bodies must be retrieved from the IMAP server, expect
                a performance hit when setting this parameter.
            include_flags: integer - Set to 1 to include IMAP flags of
                messages in the result. Since message flags must be retrieved
                from the IMAP server, expect a performance hit when setting
                this parameter.
            body_type: string - Used when include_body is set to get only body
                parts of a given MIME-type (for example text/html)
            include_source: integer - Set to 1 to include message sources in the
                result. Since message sources must be retrieved from the IMAP server,
                expect a performance hit when setting this parameter.
            sort_order: string - The sort order of the returned results.
                Possible values are asc and desc
            limit: integer - The maximum number of results to return.
            offset: integer - Start the list at this offset (zero-based).

        Returns:
            A list of Message objects.
        """
        all_args = [
            "subject", "email", "to", "sender", "from_", "cc", "bcc", "folder", "date_before",
            "date_after", "indexed_before", "indexed_after", "include_thread_size", "include_body",
            "source", "file_name", "file_size_min", "file_size_max", "include_source",
            "include_headers", "include_flags", "body_type", "sort_order",
            "limit", "offset"
        ]

        params = helpers.sanitize_params(params, all_args)

        # workaround to send param "from" even though it's a reserved keyword
        # in python
        if 'sender' in params:
            params['from'] = params['sender']
            del params['sender']

        if 'from_' in params:
            params['from'] = params['from_']
            del params['from_']

        return [
            Message(self, obj) for obj in self._request_uri('messages', params=params)]

    def get_sources(self, **params):
        """Lists IMAP sources assigned for an account.

        GET method for sources resource.

        Documentation: http://context.io/docs/2.0/accounts/sources#get

        Optional Arguments:
            status: string - Only return sources whose status is of a specific
                value. Possible statuses are: INVALID_CREDENTIALS,
                CONNECTION_IMPOSSIBLE, NO_ACCESS_TO_ALL_MAIL, OK,
                TEMP_DISABLED, and DISABLED
            status_ok: integer - Set to 0 to get sources that are not working
                correctly. Set to 1 to get those that are.

        Returns:
            A list of Source objects
        """
        all_args = ['status', 'status_ok']
        params = helpers.sanitize_params(params, all_args)

        return [Source(self, obj) for obj in self._request_uri("sources", params=params)]

    def get_sync(self):
        """Sync status for all sources of the account.

        Documentation: http://context.io/docs/2.0/accounts/sync#get

        Arguments:
            None

        Returns:
            A dictionary (see below for data structure)

        {ACCOUNT_NAME:
            {SOURCE:
                {u'last_sync_start': UNIX_TIMESTAMP,
                u'last_sync_stop': UNIX_TIMESTAMP,
                u'last_expunge': UNIX_TIMESTAMP,
                u'initial_import_finished': BOOL}
            }
        }
        """
        return self._request_uri('sync')

    def get_threads(self, **params):
        """List of threads on an account.

        Documentation: http://context.io/docs/2.0/accounts/threads#get

        Optional Arguments:
            subject: string - Get threads with messages whose subject matches
                this search string. To use regular expressions instead of
                simple string matching, make sure the string starts and ends
                with /.
            email: string - Email address of the contact for whom you want the
                latest threads. This value is interpreted as received from
                email X, sent to email X or sent by anyone to both email X and
                the source owner.
            to: string - Get threads with at least one message sent to this
                email address.
            sender: string - Get threads with at least one message sent from
                this email address.
            cc: string - Get threads with at least one message having this
                email address CC'ed.
            bcc: string - Get threads with at least one message having this
                email address BCC'ed.
            folder: string - Filter threads by the folder (or Gmail label).
                This parameter can be the complete folder name with the
                appropriate hierarchy delimiter for the mail server being
                queried (eg. Inbox/My folder) or the "symbolic name" of the
                folder (eg. \Starred). The symbolic name refers to attributes
                used to refer to special use folders in a language-independant
                way. See http://code.google.com/apis/gmail/imap/#xlist (Gmail
                specific) and RFC-6154.
            indexed_before: integer (unix time) - Get threads with at least
                one message indexed before this timestamp. This is not the
                same as the date of the email, it is the time Context.IO
                indexed this message.
            indexed_after: integer (unix time) - Get threads with at least one
                message indexed after this timestamp. This is not the same as
                the date of the email, it is the time Context.IO indexed this
                message.
            active_before: integer (unix time) - Get threads with at least one
                message dated before this timestamp. The value this filter is
                applied to is the Date: header of the message which refers to
                the time the message is sent from the origin.
            active_after: integer (unix time) - Get threads with at least one
                message dated after this timestamp. The value this filter is
                applied to is the Date: header of the message which refers to
                the time the message is sent from the origin.
            started_before: integer (unix time) - Get threads whose first
                message is dated before this timestamp. The value this filter
                is applied to is the Date: header of the message which refers
                to the time the message is sent from the origin.
            started_after: integer (unix time) - Get threads whose first
                message is dated after this timestamp. The value this filter
                is applied to is the Date: header of the message which refers
                to the time the message is sent from the origin.
            limit: integer - The maximum number of results to return.
            offset: integer - Start the list at this offset (zero-based).

        Returns:
            A list of Thread objects (nearly empty thread objects). Use the
                Thread.get() method to populate the object.
        """
        all_args = [
            'subject', 'email', 'to', 'sender', 'from_', 'cc', 'bcc', 'folder',
            'indexed_before', 'indexed_after', 'active_before', 'active_after',
            'started_before', 'started_after', 'limit', 'offset'
        ]
        params = helpers.sanitize_params(params, all_args)

        # workaround to send param "from" even though it's a reserved keyword
        # in python
        if 'sender' in params:
            params['from'] = params['sender']
            del params['sender']

        if 'from_' in params:
            params['from'] = params['from_']
            del params['from_']

        thread_urls = self._request_uri('threads', params=params)
        objs = []

        # isolate just the gmail_thread_id so we can instantiate Thread objects
        for thread_url in thread_urls:
            url_components = thread_url.split('/')
            objs.append({'gmail_thread_id': url_components[-1]})

        return [Thread(self, obj) for obj in objs]

    def get_webhooks(self):
        """Listing of WebHooks configured for an account.

        GET method for the webhooks resource.

        Documentation: http://context.io/docs/2.0/accounts/webhooks#get

        Arguments:
            None

        Returns:
            A list of Webhook objects.
        """
        return [WebHook(self, obj) for obj in self._request_uri('webhooks')]

    def post_connect_token(self, **params):
        """Obtain a new connect_token for a specific account.

        * Note: unused connect tokens are purged after 24 hours.

        Documentation: http://context.io/docs/2.0/accounts/connect_tokens#post

        Required Arguments:
            callback_url: string (url) - When the user's mailbox is connected
                to your API key, the browser will call this url (GET). This
                call will have a parameter called contextio_token indicating
                the connect_token related to this callback. You can then do a
                get on this connect_token to obtain details about the account
                and source created through that token and save that account id
                in your own user data.

        Optional Arguments:
            email: string (email) - The email address of the account to be
                added. If specified, the first step of the connect UI where
                users are prompted for their email address, first name and
                last name is skipped.
            first_name: string - First name of the account holder.
            last_name: string - Last name of the account holder.
            source_callback_url: string (url) - If specified, we'll make a
                POST request to this URL when the initial sync is completed.
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
        req_args = ['callback_url']
        all_args = [
            'callback_url', 'email', 'first_name', 'last_name', 'source_callback_url',
            'source_sync_all_folders', 'source_sync_flags', 'source_raw_file_list',
            'status_callback_url'
        ]

        return super(Account, self).post(
            uri="connect_tokens", return_bool=False, params=params, all_args=all_args,
            required_args=req_args)

    def post_email_address(self, **params):
        """Add a new email address as an alias for an account.

        Documentation: http://context.io/docs/2.0/accounts/email_addresses#post

        Required Arguments:
            email_address: string - An email address.

        Returns:
            An EmailAddress object.
        """

        response = super(Account, self).post(
            uri="email_addresses", return_bool=False, params=params, all_args=["email_address"],
            required_args=["email_address"])

        return EmailAddress(self, response)

    def post_message(self, **params):
        """Add a mesage in a given folder.

        Documentation: http://context.io/docs/2.0/accounts/messages#post

        Required Arguments:
            dst_source: string - Label of the source you want the message
                copied to
            dst_folder: string - The folder within dst_source the message
                should be copied to
            message: file - Raw RFC-822 message data. If you use the "view
                message source" function of your email client, what you'll see
                there is what we expect to receive here. Hint: you can get
                this with the accounts/messages/source call.

        Optional Arguments:
            flag_seen: integer - Message has been read. Set this parameter
                to 1 to set the flag, 0 to unset it.
            flag_answered: integer - Message has been answered. Set this
                parameter to 1 to set the flag, 0 to unset it.
            flag_flagged: integer - Message is "flagged" for urgent/special
                attention. Set this parameter to 1 to set the flag, 0 to unset it.
            flag_deleted: integer - Message is "deleted" for later removal.
                An alternative way of deleting messages is to move it to the Trash folder.
                Set this parameter to 1 to set the flag, 0 to unset it.
            flag_draft: integer - Message has not completed composition (marked as a draft).
                Set this parameter to 1 to set the flag, 0 to unset it.

        Returns:
            Bool
        """
        headers = {"Content-Type": "multipart/form-data"}

        req_args = ["dst_source", "dst_folder", "message"]

        all_args = [
            "dst_source", "dst_folder", "message", "flag_seen", "flag_answered", "flag_flagged",
            "flag_deleted", "flag_draft"
        ]

        return super(Account, self).post(
            uri="messages", return_bool=False, params=params, headers=headers, all_args=all_args,
            required_args=req_args)

    def post_source(self, **params):
        """Add a mailbox to a given account.

        Documentation: http://context.io/docs/2.0/accounts/sources#post

        Required Arguments:
            email: string - The primary email address used to receive emails
                in this account
            server: string - Name of IP of the IMAP server, eg. imap.gmail.com
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
            A mostly empty Source object or False if something failed.
        """
        # set some default values
        if 'use_ssl' not in params:
            params['use_ssl'] = 1
        if 'port' not in params:
            params['port'] = 993
        if 'type' not in params:
            params['type'] = 'IMAP'

        req_args = ['email', 'server', 'username', 'port', 'type', 'use_ssl']
        all_args = [
            'email', 'server', 'username', 'port', 'type', 'use_ssl',
            'origin_ip', 'expunge_on_deleted_flag', 'sync_all_folders',
            'sync_folders', 'sync_flags', 'raw_file_list', 'password',
            'provider_refresh_token', 'provider_consumer_key',
            'callback_url', 'status_callback_url'
        ]

        data = super(Account, self).post(
            uri="sources", return_bool=False, params=params, all_args=all_args,
            required_args=req_args
        )

        if data.get("success") is False:
            return False

        return Source(self, {'label': data['label']})

    def post_sync(self):
        """Trigger a sync of all sources on the account.

        Documentation: http://context.io/docs/2.0/accounts/sync#post

        Arguments:
            None

        Returns:
            A dictionary (see below for data structure)

            {
                u'syncs_queued': STRING,
                u'resource_url': STRING,
                u'success': BOOL
            }
        """
        return self._request_uri("sync", method="POST")

    def post_webhook(self, **params):
        """Create a new WebHook on an account.

        POST method for the webhooks resource.

        Documentation: http://context.io/docs/2.0/accounts/webhooks#post

        Required Arguments:
            callback_url: string (url) - A valid URL Context.IO calls when a
                matching message is found.
            failure_notif_url: string (url) - A valid URL Context.IO calls
                if the WebHooks fails and will no longer be active. That may
                happen if, for example, the server becomes unreachable or if
                it closes an IDLE connection and we can't re-establish it.

        Optional Arguments:
            filter_to: string - Check for new messages sent to a given name or
                email address.
            filter_from: string - Check for new messages received from a given
                name or email address.
            filter_cc: string - Check for new messages where a given name or
                email address is cc'ed
            filter_subject: string - Check for new messages with a subject
                matching a given string or regular expresion
            filter_thread: string - Check for new messages in a given thread.
                Value can be a gmail_thread_id or the email_message_id or
                message_id of an existing message currently in the thread.
            filter_new_important: string - Check for new messages
                automatically tagged as important by the Gmail Priority Inbox
                algorithm. To trace all messages marked as important
                (including those manually set by the user), use
                filter_folder_added with value Important. Note the leading
                back-slash character in the value, it is required to keep this
                specific to Gmail Priority Inbox. Otherwise any message placed
                in a folder called "Important" would trigger the WebHook.
            filter_file_name: string - Check for new messages where a file
                whose name matches the given string is attached. Supports
                wildcards and regular expressions like the file_name parameter
                of the files list call.
            filter_folder_added: string - Check for messages filed in a given
                folder. On Gmail, this is equivalent to having a label applied
                to a message. The value should be the complete name (including
                parents if applicable) of the folder you want to track.
            filter_folder_removed: string - Check for messages removed from a
                given folder. On Gmail, this is equivalent to having a label
                removed from a message. The value should be the complete name
                (including parents if applicable) of the folder you want to
                track.
            filter_to_domain: string - Check for new messages sent to a given
                domain. Also accepts a comma delimited list of domains.
            filter_from_domain: string - Check for new messages sent from a given
                domain. Also accepts a comma delimited list of domains.
            include_body: integer - Set to 1 to include the message body in
                the result. Since the body must be retrieved from the IMAP
                server, expect a performance hit when setting this parameter.
            body_type: string - Used when include_body is set to get only body
                parts of a given MIME-type (for example text/html)

        Returns:
            A mostly empty WebHook object if successful, or False
        """
        req_args = ['callback_url', 'failure_notif_url']
        all_args = [
            'callback_url', 'failure_notif_url', 'filter_to', 'filter_from',
            'filter_cc', 'filter_subject', 'filter_thread',
            'filter_new_important', 'filter_file_name', 'filter_folder_added',
            'filter_folder_removed', 'filter_to_domain', 'filter_from_domain',
            'include_body', 'body_type', 'include_parsed_receipts'
        ]

        webhook = super(Account, self).post(
            uri="webhooks", params=params, return_bool=False, all_args=all_args, required_args=req_args)

        if bool(webhook['success']) is False:
            return False

        return WebHook(self, {'webhook_id': webhook['webhook_id']})

