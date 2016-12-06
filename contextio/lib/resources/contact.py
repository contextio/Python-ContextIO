from __future__ import absolute_import
import logging

from .. import helpers
from .base_resource import BaseResource
from .file import File
from .message import Message
from .thread import Thread

class Contact(BaseResource):
    """Class to represent the Contact resource.

    Properties:
        emails: list of strings (email) - Array of email addresses for this
            contact
        name: string - Full name of contact
        thumbnail: string (url) - URL pointing to Gravatar image associated to
            contact's email address, if applicable
        last_received: integer - Unix timestamp of date the last message was
            received
        last_sent: integer - Unix timestamp of date the last message was sent
        count: integer - Number of emails exchanged with this contact
        sent_count: integer - number of messages that include the contact in To, CC, or BCC
        received_count: integer - number of messages that include the contact in From
        sent_from_account_count: integer - number of messages that include the contact in
            To, CC, or BCC and an email from this account in From
        email: string (email) - one of the contact's email addresses
    """
    resource_id = "email"
    keys = ["emails", "name", "thumbnail", "last_received", "last_sent",
        "count", "sent_count", "received_count", "sent_from_account_count", "email"]

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: Account object - parent is an Account object.
            definition: a dictionary of parameters. The 'email' parameter is
                required to make method calls.
        """

        super(Contact, self).__init__(parent, 'contacts/{email}',  definition)

        if definition.get("emails") is None:
            self.emails = [definition['email']]

    def get(self):
        """Retrieves information about given contact.

        Documentation: http://context.io/docs/2.0/accounts/contacts#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        # since the data returned doesn't have an email key, add it from emails
        # cannot use the BaseResource get method here =/
        data = self._request_uri()
        if data.get("email") is None:
            emails = data.get("emails")
            if emails is not None and len(emails) > 0:
                data['email'] = data['emails'][0]

        self.__init__(self.parent, data)
        return True

    def put(self):
        logging.info("This method is not implemented")

    def post(self):
        logging.info("This method is not implemented")

    def delete(self):
        logging.info("This method is not implemented")

    def get_files(self, **params):
        """List files exchanges with a contact.

        Documentation: http://context.io/docs/2.0/accounts/contacts/files#get

        Optional Arguments:
            limit: integer - The maximum number of results to return.
            offset: integer - Start the list at this offset (zero-based).

        Returns:
            A list of File objects
        """
        all_args = ['limit', 'offset']
        params = helpers.sanitize_params(params, all_args)

        return [File(self.parent, obj) for obj in self._request_uri('files', params=params)]

    def get_messages(self, **params):
        """List messages where a contact is present.

        Documentation:
            http://context.io/docs/2.0/accounts/contacts/messages#get

        Optional Arguments:
            limit: integer - The maximum number of results to return.
            offset: integer - Start the list at this offset (zero-based).

        Returns:
            A list of Message objects
        """
        all_args = ['limit', 'offset']
        params = helpers.sanitize_params(params, all_args)

        return [Message(self.parent, obj) for obj in self._request_uri('messages', params=params)]

    def get_threads(self, **params):
        """List threads where contact is present.

        Documentation: http://context.io/docs/2.0/accounts/contacts/threads#get

        Optional Arguments:
            limit: integer - The maximum number of results to return.
            offset: integer - Start the list at this offset (zero-based).

        Returns:
            A list of Thread objects.
        """
        all_args = ['limit', 'offset']
        params = helpers.sanitize_params(params, all_args)

        thread_urls = self._request_uri('threads', params=params)
        objs = []

        # isolate just the gmail_thread_id so we can instantiate Thread objects
        for thread_url in thread_urls:
            url_components = thread_url.split('/')
            objs.append({'gmail_thread_id': url_components[-1]})

        return [Thread(self.parent, obj) for obj in objs]
