from __future__ import absolute_import
import logging

from .base_resource import BaseResource

class EmailAddress(BaseResource):
    """Class to represent the EmailAddress resource.

    Properties:
        email: string - Email address associated to an account.
        validated: integer - Unix timestamp of email address validation time
        primary: integer - whether or not this address is the primary one
            associated to the account. 1 for yes, 0 for no.
    """
    resource_id = "email"
    keys = ["email", "validated", "primary"]

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: Account object - parent is an Account object.
            definition: a dictionary of parameters. The 'email' parameter is
                required to make method calls.
        """
        # allow devs to use email_address instead of email argument
        if definition.get("email_address") is not None:
            definition['email'] = definition['email_address']

        super(EmailAddress, self).__init__(parent, 'email_addresses/{email}', definition)

    def get(self):
        """GET details for a given email address.

        GET method for the email_addresses resource.

        Documentation:
            http://context.io/docs/2.0/accounts/email_addresses#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        return super(EmailAddress, self).get()

    def post(self, primary=None, **params):
        """Modifies a given email address.

        POST method for the email_addresses resource.

        Documentation:
            http://context.io/docs/2.0/accounts/email_addresses#id-post

        Optional Arguments:
            primary: int - Set to 1 to make this email address the primary one
                for the account

        Returns:
            Bool
        """
        # update EmailAddress object with new values
        if primary is not None:
            self.primary = int(primary)

        return super(EmailAddress, self).post(params=params, all_args=["primary"])

    def delete(self):
        """Remove a given email address.

        DELETE method for the email_addresses resource.

        Documentation: http://context.io/docs/2.0/accounts/email_addresses#id-delete

        Arguments:
            None

        Returns:
            Bool
        """
        return super(EmailAddress, self).delete()


    def put(self):
        logging.info("This method is not implemented")
