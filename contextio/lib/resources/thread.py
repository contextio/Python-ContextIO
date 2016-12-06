from __future__ import absolute_import

import logging

from .base_resource import BaseResource

class Thread(BaseResource):
    """Class to represent the thread resource.

    Properties:
        gmail_thread_id: string - Thread id assigned by Gmail (only present if
            source is a Gmail account)
        email_message_ids: list of strings - List of email_message_ids forming
            the thread
        person_info: dict - Additional info about contacts on this message
        messages: list of Message objects
        subject: string - Subject of the message
        folders: list - List of folders (or Gmail labels) this message is
            found in
        sources: list of Source objects
    """
    resource_id = "gmail_thread_id"
    keys = [
        "gmail_thread_id", "email_message_ids", "person_info", "messages", "subject", "folders",
        "sources"
    ]

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: Account object - parent is an Account object.
            definition: a dictionary of parameters. The 'gmail_thread_id' parameter
                is required to make method calls.
        """
        super(Thread, self).__init__(parent, 'threads/{gmail_thread_id}', definition)

        # This is going to be gross - prepare yourself

        if "messages" in definition:
            from contextio.lib.resources.message import Message
            self.messages = [
                Message(self.parent, message) for message in definition['messages']
            ]

        if 'sources' in definition:
            from contextio.lib.resources.source import Source
            self.sources = [
                Source(self.parent, source) for source in definition['sources']
            ]

    def get(self, **params):
        """Returns files, contacts, and messages on a given thread.

        Documentation: http://context.io/docs/2.0/accounts/threads#id-get

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
            True if self is updated, else will throw a request error
        """
        all_args = [
            'include_body', 'include_headers', 'include_flags', 'body_type', 'limit', 'offset'
        ]

        return super(Thread, self).get(self.parent, params=params, all_args=all_args)


    def put(self):
        logging.info("This method is not implemented")

    def post(self):
        logging.info("This method is not implemented")

    def delete(self):
        logging.info("This method is not implemented")
