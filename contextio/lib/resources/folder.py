from __future__ import absolute_import
import logging

from .. import helpers
from .base_resource import BaseResource
from .message import Message


class Folder(BaseResource):
    """Class to represent the Folder resource.

    Properties:
        name: string - Name of the folder
        attributes: dictionary - IMAP Attributes of the folder given as a hash
        delim: string - Character used to delimite hierarchy in the folder name
        nb_messages: integer - Number of messages found in this folder
        nb_unseen_messages: integer - Number of unread messages in this folder
            (present only if include_extended_counts is set to 1)
    """
    resource_id = "name"
    keys = {
        "2.0": ["name", "attributes", "delim", "nb_messages", "nb_unseen_messages"],
        "lite": ["name", "attributes", "delimiter", "nb_messages", "nb_unseen_messages"]
    }


    def __init__(self, parent, defn):
        """Constructor.

        Required Arguments:
            parent: Source object - parent is an Source object.
            defn: a dictionary of parameters. The 'name' parameter is
                required to make method calls.
        """
        super(Folder, self).__init__(parent, 'folders/{name}', defn)

    def get(self):
        """Information about a given folder.

        Documentation:
            http://context.io/docs/2.0/accounts/sources/folders#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        return super(Folder, self).get()

    def put(self, **params):
        """Create a folder on an IMAP source.

        Documentation:
            http://context.io/docs/2.0/accounts/sources/folders#id-put

        Optional Arguments:
            delim: string - If / isn't fancy enough as a hierarchy delimiter
                when specifying the folder you want to create, you're free to
                use what you want, just make sure you set this delim parameter
                to tell us what you're using.

        Returns:
            Bool
        """
        all_args = ["delim"]
        params = helpers.sanitize_params(params, all_args)
        status = self._request_uri(method="PUT", params=params)
        return bool(status["success"])

    def post(self):
        logging.info("This method is not implemented")

    def delete(self):
        """Remove a given folder.

        DELETE method for the folder resource.

        Documentation:

        Arguments:
            None

        Returns:
            Bool
        """
        return super(Folder, self).delete()

    def get_messages(self, **params):
        """Get current listings of email messages in a given folder.

        NOTE: this gets all messages including since last sync. It's fresher,
            but expect slower performance than using Account.get_messages()

        Documentation:
            http://context.io/docs/2.0/accounts/sources/folders/messages#get

        Optional Arguments:
            include_thread_size: integer - Set to 1 to include thread size in
                the result.
            include_body: integer - Set to 1 to include message bodies in the
                result. Since message bodies must be retrieved from the IMAP
                server, expect a performance hit when setting this parameter.
            body_type: string - Used when include_body is set to get only body
                parts of a given MIME-type (for example text/html)
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
            flag_seen: integer - Set to 1 to restrict list to messages having
                the \Seen flag set, set to 0 to have the messages with that
                flag unset (ie. list unread messages in the folder).
            limit: integer - The maximum number of results to return.
            offset: integer - Start the list at this offset (zero-based).

        Returns:
            a list of Message objects.
        """
        all_args = [
            "include_thread_size", "include_body",
            "body_type", "include_headers", "include_flags", "flag_seen",
            "limit", "offset"
        ]
        params = helpers.sanitize_params(params, all_args)

        return [
            Message(self, obj) for obj in self._request_uri('messages', params=params)
        ]
