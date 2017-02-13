from __future__ import absolute_import
import logging

from .base_resource import BaseResource

class File(BaseResource):
    """Class to represent the File resource.

    Properties:
        size: integer - size of file in bytes.
        type: string - MIME type as specified in message source
        subject: string - Subject line of message this file is attached to
        date: integer - Unix timestamp of the message
        date_indexed: integer - Time this message was first seen by Context.IO
            (unix timestamp)
        addresses: dict - Email addresses and names of sender and recipients
        person_info: dict - Additional info about contacts on the message
        file_name: string - Name of file
        file_name_structure: list - Name of the file broken down in semantic
            parts
        body_section: integer - IME section this file can be found in
            (useful only if you're parsing raw source)
        file_id: string - Unique and persistent id for this file
        supports_preview: bool - whether or not the file supports our preview
            function
        is_embedded: bool - Indicates whether this file is an object embedded
            in the message or not
        content_disposition: string - Value of the Content-Disposition header
            of the MIME part containing this file, if specified. Typically
            'inline' or 'attachment'
        content_id: string - If this file is an embedded object, this is the
            value of the Content-Id header of the MIME part containing this
            file
        message_id: string - Context.IO id of the message this file is
            attached to
        email_message_id: string - Value of RFC-822 Message-ID header this
            file is attached to
        gmail_message_id: string - Gmail message id the file is attached to
            (only present if source is a Gmail account)
        gmail_thread_id: string - Gmail thread id the file is attached to
            (only present if source is a Gmail account)
        """
    resource_id = "file_id"
    keys = ['size', 'type', 'subject', 'date', 'date_indexed', 'addresses',
        'person_info', 'file_name', 'file_name_structure', 'body_section',
        'file_id', 'supports_preview', 'is_embedded', 'content_disposition',
        'content_id', 'message_id', 'email_message_id', 'gmail_message_id',
        'gmail_thread_id']

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: Account object - parent is an Account object.
            definition: a dictionary of parameters. The 'file_id' parameter is
                required to make method calls.
        """

        super(File, self).__init__(parent, "files/{file_id}", definition)

    def get(self):
        """GET details for a given file.

        GET method for the files resource.

        Documentation: http://context.io/docs/2.0/accounts/files#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        return super(File, self).get()

    def put(self):
        logging.info("This method is not implemented")

    def post(self):
        logging.info("This method is not implemented")

    def delete(self):
        logging.info("This method is not implemented")

    def get_content(self, download_link=False):
        """Download a file.

        Documentation: http://context.io/docs/2.0/accounts/files/content

        Optional Arguments:
            download_link: bool - False by default, if True, returns a link
                rather than the file

        Returns:
            Binary if getting content, String if getting download url
        """
        if download_link:
            headers = {
                'Accept': 'text/uri-list'
            }
        else:
            headers = {}

        return self._request_uri('content', headers=headers)

    def get_related(self):
        """Get list of other files related to a given file.

        Documentation: http://context.io/docs/2.0/accounts/files/related#get

        Arguments:
            None

        Returns:
            A list of File objects.
        """
        return [File(self, obj) for obj in self._request_uri("related")]

