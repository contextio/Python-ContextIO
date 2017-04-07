from .. import helpers
from .base_resource import BaseResource, only
from .file import File
from .thread import Thread


class Message(BaseResource):
    """Class to represent the Message resource.

    Properties:
        date: integer - Unix timestamp of message date
        date_indexed: integer (unix timestamp) - Time this message was first
            seen by Context.IO
        addresses: dict - Email addresses and names of sender and recipients
        person_info: dict - Additional info about contacts on this message
        email_message_id: string - Value of RFC-822 Message-ID header
        message_id: string - Unique and persistent id assigned by Context.IO
            to the message
        gmail_message_id: string - Message id assigned by Gmail (only present
            if source is a Gmail account)
        gmail_thread_id: string - Thread id assigned by Gmail (only present if
            source is a Gmail account)
        files: list of File objects
        subject: string - Subject of the message
        folders: list - List of folders (or Gmail labels) this message is
            found in
        sources: list of dicts
        body: list of dicts - Each dict represents a MIME part.
        flags: dict - the flags for this message
        folders: dict - the folders this message is in
    """
    resource_id = "message_id"
    keys = {
        "2.0": [
            "date", "date_indexed", "date_received", "addresses", "person_info", "email_message_id", "message_id",
            "gmail_message_id", "gmail_thread_id", "files", "subject", "folders", "sources"
        ],
        "lite": [
            "sent_at", "addresses", "subject", "email_message_id", "message_id", "list_headers",
            "in_reply_to", "references", "attachments", "bodies", "received_headers", "folders",
            "resource_url", "person_info"
        ]
    }

    # set empty properties that will get populated by the get methods
    body = None
    flags = None
    headers = None

    # 2.0 only
    folders = None
    source = None
    thread = None

    # lite only
    raw = None
    attachments = None

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: Account object - parent is an Account object.
            definition: a dictionary of parameters. The 'message_id' parameter is
                required to make method calls.
        """

        super(Message, self).__init__(parent, 'messages/{message_id}', definition)

        if 'files' in definition:
            self.files = [File(self.parent, file) for file in definition['files']]

        # some calls optionally return a message with some extra data
        if 'body' in definition:
            self.body = definition['body']
        if 'flags' in definition:
            self.flags = definition['flags']
        if 'headers' in definition:
            self.headers = definition['headers']

    def get(self, **params):
        """Get file, contact and other information about a given email message.

        Documentation: http://context.io/docs/2.0/accounts/messages#id-get

        Optional Arguments:
            include_thread_size: integer - Set to 1 to include thread size in the result.
            include_body: integer - Set to 1 to include the message body in
                the result. Since the body must be retrieved from the IMAP
                server, expect a performance hit when setting this parameter.
            include_headers: mixed - Can be set to 0 (default), 1 or raw. If
                set to 1, complete message headers, parsed into an array, are
                included in the results. If set to raw, the headers are also
                included but as a raw unparsed string. Since full original
                headers bodies must be retrieved from the IMAP server, expect
                a performance hit when setting this parameter.
            include_flags: integer - Set to 1 to include IMAP flags for this
                message in the result. Since message flags must be retrieved
                from the IMAP server, expect a performance hit when setting
                this parameter.
            body_type: string - Used when include_body is set to get only body
                parts of a given MIME-type (for example text/html)
            include_source: integer - Set to 1 to include message sources in the
                result. Since message sources must be retrieved from the IMAP
                server, expect a performance hit when setting this parameter.

        Returns:
            True if self is updated, else will throw a request error
        """
        all_args = [
            "include_thread_size", "include_body", "include_headers", "include_flags", "body_type",
            "include_source"
        ]

        return super(Message, self).get(params=params, all_args=all_args)

    @only("lite")
    def put(self, **params):
        """Get file, contact and other information about a given email message.

        Documentation: http://context.io/docs/2.0/accounts/messages#id-get

        Optional Arguments:

        Returns:
            True if self is updated, else will throw a request error
        """
        all_args = ["new_folder_id", "delimiter"]

        return super(Message, self).get(params=params, all_args=all_args)

    def post(self, return_bool=True, **params):
        """Copy or move a message.

        Documentation: http://context.io/docs/2.0/accounts/messages#id-post

        Required Arguments:
            dst_folder: string - The folder within dst_source the message
                should be copied to

        Optional Arguments:
            dst_source: string - Label of the source you want the message
                copied to. This field is required if you're moving a message
                that already exists in one source of the account to another
                source of that account. If you only want to move the message
                to a different folder within the same source, dst_folder is
                sufficient.
            move: integer - By default, this calls copies the original message
                in the destination. Set this parameter to 1 to move instead of
                copy.
            flag_seen: integer - Message has been read. Set this parameter to
                1 to set the flag, 0 to unset it.
            flag_answered: integer - Message has been answered. Set this parameter
                to 1 to set the flag, 0 to unset it.
            flag_flagged: integer - Message is "flagged" for urgent/special attention.
                Set this parameter to 1 to set the flag, 0 to unset it.
            flag_deleted: integer - Message is "deleted" for later removal. An
                alternative way of deleting messages is to move it to the Trash
                folder. Set this parameter to 1 to set the flag, 0 to unset it.
            flag_draft: integer - Message has not completed composition (marked as
                a draft). Set this parameter to 1 to set the flag, 0 to unset it.
        Returns:
            Bool, unless return_bool parameter is set to False, then returns
                dict
        """

        req_args = ['dst_folder', ]
        all_args = ['flag_answered', 'move', 'dst_folder', 'dst_source', 'flag_seen',
            'flag_flagged', 'flag_deleted', 'flag_draft']

        return super(Message, self).post(return_bool=return_bool, params=params, all_args=all_args, required_args=req_args)

    def delete(self):
        """Delete a message.

        Documentation: http://context.io/docs/2.0/accounts/messages#id-delete

        Arguments:
            None
        Returns:
            Bool
        """
        return super(Message, self).delete()

    def get_body(self, **params):
        """Fetch the message body of a given email.

        This method sets self.body, and returns a data structure.

        Documentation: http://context.io/docs/2.0/accounts/messages/body#get

        Optional Arguments:
            type: string - Many emails are sent with both rich text and plain
                text versions in the message body and by default, the response
                of this call will include both. It is possible to only get
                either the plain or rich text version by setting the type
                parameter to text/plain or text/html respectively.

        Returns:
            a list of dictionaries, data format below

            [
              {
                "type": string - MIME type of message part being fetched,
                "charset": string - encoding of the characters in the part of
                    message,
                "content": string - the actual content of the message part
                    being pulled,
                "body_section": number - indicating position of the part in
                    the body structure,
              }
            ]
        """
        all_args = ['type']
        params = helpers.sanitize_params(params, all_args)
        self.body = self._request_uri("body", params=params)
        return self.body

    def get_flags(self):
        """Get message flags.

        This method sets self.flags, and returns a data structure.

        Documentation: http://context.io/docs/2.0/accounts/messages/flags#get

        Arguments:
            None

        Returns:
            A dictionary, data format below

            {
              "seen": boolean - whether or not a message has been viewed,
              "answered": boolean - whether or not a message has been
                  replied to,
              "flagged": boolean - whether or not a message has been flagged,
              "deleted": boolean - whether or not a message has been deleted,
              "draft": boolean - whether or not a message is in draft mode,
              "nonjunk": boolean - whether or not a message has been flagged
                  as "junk" mail,
            }
        """
        self.flags = self._request_uri("flags")
        return self.flags

    @only("2.0")
    def post_flag(self, **params):
        """Set message flags for a given email.

        Also, populates/updates self.flags with the new data.

        Optional Arguments:
            seen: integer - Message has been read. Set this parameter to 1 to
                set the flag, 0 to unset it.
            answered: integer - Message has been answered. Set this parameter
                to 1 to set the flag, 0 to unset it.
            flagged: integer - Message is "flagged" for urgent/special
                attention. Set this parameter to 1 to set the flag, 0 to unset
                it.
            deleted: integer - Message is "deleted" for later removal. An
                alternative way of deleting messages is to move it to the
                Trash folder. Set this parameter to 1 to set the flag, 0 to
                unset it.
            draft: integer - Message has not completed composition (marked as
                a draft). Set this parameter to 1 to set the flag, 0 to unset
                it.

        Returns:
            Bool, after setting self.flags.
        """
        all_args = ["seen", "answered", "flagged", "deleted", "draft"]
        params = helpers.sanitize_params(params, all_args)

        data = self._request_uri("flags", method="POST", params=params)
        status = bool(data["success"])

        if status:
            self.flags = data["flags"]

        return status

    @only("2.0")
    def get_folders(self):
        """List of folders a message is in.

        This method sets self.folders, and returns a data structure.

        Documentation: http://context.io/docs/2.0/accounts/messages/folders#get

        Arguments:
            None

        Returns:
            A list of dicts, data format below.

            [
              {
                "name": string - Name of an IMAP folder,
                "symbolic_name": string - Special-use attribute of this folder
                    (if and only if the server supports it and applicable to
                    this folder)
              },
              ...
            ]
        """
        self.folders = self._request_uri('folders')
        return self.folders

    @only("2.0")
    def post_folder(self, **params):
        """Edits the folders a message is in.

        This call supports adding and/or removing more than one folder
            simultaneously using the [] suffix to the parameter name.

        Documentation:
            http://context.io/docs/2.0/accounts/messages/folders#post

        Optional Arguments:
            add: string - New folder this message should appear in.
            remove: string - Folder this message should be removed from.

        Returns:
            Bool
        """
        all_args = ['add', 'remove', 'add[]', 'remove[]']
        params = helpers.sanitize_params(params, all_args)
        return super(Message, self).post("folders", params=params)

    @only("2.0")
    def put_folders(self, body):
        """Set folders a message should be in.

        Documentation: http://context.io/docs/2.0/accounts/messages/folders#put

        Required Arguments:
            body: string - The format of the request body follows the format
                of the GET response above with the exception that you only
                need to specify either the name or symbolic_name property for
                each folder the message must appear in. As shown in the
                example below, if you want to set folders using the symbolic
                names as returned by the XLIST command, make sure you escape
                the \ character.

                [{"name":"my personal label"},{"symbolic_name":"\\Starred"},
                {"name":"parent folder/child folder"}]

        Returns:
            Bool
        """
        status = self._request_uri("folders", method="PUT", body=body)
        status = bool(status['success'])

        if status:
            self.folders = body

        return status

    def get_headers(self, **params):
        """Get complete headers for a message.

        Documentation: http://context.io/docs/2.0/accounts/messages/headers#get

        Optional Arguments:
            raw: integer - By default, this returns messages headers parsed
                into an array. Set this parameter to 1 to get raw unparsed
                headers.

        Returns:
            Dict, data structure below.

            {
              Name-Of-Header: array - Values for that header (some headers can
                  appear more than once in the message source),
              ...
            }
        """
        all_args = ['raw']
        params = helpers.sanitize_params(params, all_args)
        self.headers = self._request_uri('headers', params=params)
        return self.headers

    @only("2.0")
    def get_source(self):
        """Get the message source.

        Documentation: http://context.io/docs/2.0/accounts/messages/source#get

        Arguments:
            None

        Returns:
            string - raw RFC-822 message
        """
        self.source = self._request_uri('source')
        return self.source

    @only("2.0")
    def get_thread(self, **params):
        """List other messages in the same thread as this message.

        Documentation: http://context.io/docs/2.0/accounts/messages/thread#get

        Optional Arguments:
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
            limit: integer - The maximum number of messages to include in the
                messages property of the response.
            offset: integer - Start the list of messages at this offset
                (zero-based).

        Returns:
            a Thread object. Unless we can't find a thread id, then just the
                response
        """
        all_args = [
            "include_body", "include_headers", "include_flags", "body_type",
            "limit", "offset"
        ]
        params = helpers.sanitize_params(params, all_args)

        data = self._request_uri("thread", params=params)

        # try to find the gmail_thread_id
        gmail_thread_id = None
        messages = data.get("messages")
        if messages is not None:
            first_message = messages[0]
            gmail_thread_id = first_message.get("gmail_thread_id")
            if gmail_thread_id:
                data["gmail_thread_id"] = "gm-{0}".format(gmail_thread_id)

        self.thread = Thread(self.parent, data) if gmail_thread_id else data

        # if we have the subject, set thread.subject
        if self.subject and self.thread:
            self.thread.subject = self.subject

        return self.thread

    @only("lite")
    def get_raw(self, **params):
        all_args = ['delimiter']
        params = helpers.sanitize_params(params, all_args)
        self.raw = self._request_uri('raw', params=params)

    @only("lite")
    def get_attachments(self, **params):
        all_args = ['delimiter']
        params = helpers.sanitize_params(params, all_args)
        self.attachments = self._request_uri('attachments', params=params)

    @only("lite")
    def post_read(self, **params):
        all_args = ["delimiter"]
        params = helpers.sanitize_params(params, all_args)
        return super(Message, self).post("read", params=params)

    @only("lite")
    def delete_read(self, **params):
        all_args = ["delimiter"]
        params = helpers.sanitize_params(params, all_args)
        return super(Message, self).delete("read")
