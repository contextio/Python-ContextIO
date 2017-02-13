from __future__ import absolute_import
from six import string_types
import logging

from .base_resource import BaseResource


class ConnectToken(BaseResource):
    """Class to represent the connect_token resource.

    Properties:
        token: string - Id of the connect_token
        email: string - email address specified on token creation
        created: integer - Unix timestamp of the connect_token was created
        used: integer - Unix time this token was been used. 0 means it no
            account has been created with this token yet
        expires: mixed - Unix time this token will expire and be purged. Once
            the token is used, this property will be set to false
        callback_url: string - URL of your app we'll redirect the browser to
            when the account is created
        first_name: string - First name specified on token creation
        last_name: string - Last name specified on token creation
        account: Account object
    """
    resource_id = "token"
    keys = {
        "2.0": [
            "token", "email", "created", "used", "expires", "callback_url",
            "first_name", "last_name", "account"
        ],
        "lite": [
            "token", "email", "account_lite", "created", "used", "status_callback_url",
            "callback_url", "first_name", "last_name", "email_account_id", "resource_url", "expires"
        ]
    }

    def __init__(self, parent, definition):
        """Constructor.

        Required Arguments:
            parent: ContextIO object - parent is an ContextIO object.
            definition: a dictionary of parameters. The 'token' parameter is
                required to make method calls.
        """
        super(ConnectToken, self).__init__(parent, 'connect_tokens/{token}', definition)

        self.account = self._create_account(definition.get("account"))
        self.user = self._create_user(definition.get("user"))

    def _create_account(self, account):
        # yes this is gross
        if account is not None and len(account) > 0:
            pass
            if isinstance(account, string_types):
                account_details = {"id": account}
            else:
                account_details = account

            from contextio.lib.resources.account import Account
            return Account(self.parent, account_details)
        else:
            return None

    def _create_user(self, user):
        if user is not None:
            from contextio.lib.resources.user import User
            return User(self.parent, user)
        else:
            return None

    def get(self):
        """Information about a given connect token.

        Documentation:
            http://context.io/docs/2.0/accounts/connect_tokens#id-get

        Arguments:
            None

        Returns:
            True if self is updated, else will throw a request error
        """
        return super(ConnectToken, self).get()

    def delete(self):
        """Remove a given connect token.

        Documentation:
            http://context.io/docs/2.0/accounts/connect_tokens#id-delete

        Arguments:
            None

        Returns:
            Bool
        """
        return super(ConnectToken, self).delete()

    def put(self):
        logging.info("This method is not implemented")

    def post(self):
        logging.info("This method is not implemented")
