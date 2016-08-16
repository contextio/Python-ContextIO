import pkg_resources
import logging
import six
from rauth import OAuth1Session

from contextio.lib import helpers
from contextio.lib.errors import RequestError
from contextio.lib.resources.connect_token import ConnectToken
from contextio.lib.resources.discovery import Discovery
from contextio.lib.resources.oauth_provider import OauthProvider

class Api(object):

    """Parent class of module. This handles authentication and requests.

    Parameters:
        consumer_key: string - your Context.IO consumer key
        consumer_secret: string - your Context.IO consumer secret
        debug: string - Set to None by default. If you want debug messages,
            set to either 'print' or 'log'. If set to 'print', debug messages
            will be printed out. Useful for python's interactive console. If
            set to 'log' will send debug messages to logging.debug()
    """

    def __init__(self, consumer_key, consumer_secret, debug=None, api_version="2.0", **kwargs):
        """Constructor that creates oauth2 consumer and client.

        Required Arguments:
            consumer_key: string - your api key
            consumer_secret: string - you api secret

        Optional Arguments:
            debug: if used, set to either 'print' or 'log' - if print, debug
                messages will be sent to stdout. If set to 'log' will send
                to logging.debug()
        """
        self.url_base = kwargs.get("url_base")

        if self.url_base is None:
            self.url_base = "https://api.context.io"

        self.api_version = api_version

        self.debug = debug
        if self.debug is True:   # for people who don't read the code and just set debug=True
            self.debug = "print"

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.session = OAuth1Session(self.consumer_key, self.consumer_secret)

    def _debug(self, response):
        """Prints or logs a debug message.

        Required Arguments:
            response: object - the rauth response object.

        Returns:
            None
        """

        if self.debug:
            message = (
                "--------------------------------------------------\n"
                "URL:    {0}\nMETHOD: {1}\nSTATUS: 2\n\nREQUEST\n{3}\n\n"
                "RESPONSE\n{4}\n").format(
                    response.request.url, response.request.method, response.status_code,
                    response.request.__dict__, response.__dict__)

            if self.debug == "print":
                six.print_(message)
            elif self.debug == "log":
                logging.debug(message)

    def _request_uri(self, uri="", method="GET", params={}, headers={}, body=""):
        """Assembles the request uri and calls the request method.

        Required Arguments:
            uri: string - the assembled API endpoint.

        Optional Parameters:
            method: string - the method of the request. Possible values are
                'GET', 'POST', 'DELETE', 'PUT'
            params: dict - parameters to pass along
            headers: dict - any specific http headers
            body: string - request body, only used on a few PUT statements

        Returns:
            typically, JSON - depends on the API call, refer to the other
                method docstrings for more details.
        """
        url = "/".join((self.url_base, self.api_version, uri))

        try:
            lib_version = pkg_resources.require("contextio")[0].version
        except:
            lib_version = "dev"

        headers.update(
            {"user-agent": "contextio/{0}/python-lib-{1}".format(self.api_version, lib_version)})

        if method == "POST":
            params['body'] = body
            response = self.session.request(
                method, url, header_auth=True, data=params, headers=headers)
        else:
            response = self.session.request(
                method, url, header_auth=True, params=params, headers=headers, data=body)

        self._debug(response)
        try:
            response_body = response.json()
        except UnicodeDecodeError:
            response_body = response.content
        except ValueError:
            response_body = response.text

        if response.status_code >= 200 and response.status_code < 300:
            return response_body
        else:
            raise RequestError(
                "Request to {0} failed with HTTP status code {1}: {2}".format(
                    url, response.status_code, response_body), response=response)

    # THE FOLLOWING ROUTES ARE COMMON TO BOTH LITE AND 2.0
    def get_connect_tokens(self, **params):
        """Get a list of connect tokens created with your API key.

        2.0
        Documentation: http://context.io/docs/2.0/connect_tokens#get

        Lite
        Documentation: http://context.io/docs/lite/connect_tokens#get

        Optional Arguments:
            token : string - The connect token used to create the account .

        Making the api call https://context.io/2.0/connect_tokens/<token_id>

        Returns(if token is given):

        A dictionary :

        {
          "token": stringId of the connect_token,
          "email": stringemail address specified on token creation,
          "created": numberUnix timestamp of the connect_token was created,
          "used": numberUnix time this token was been used. 0 means it no account has been created with this token yet,
          "expires": mixedUnix time this token will expire and be purged. Once the token is used, this property will be set to false,
          "callback_url": stringURL of your app we'll redirect the browser to when the account is created,
          "first_name": stringFirst name specified on token creation,
          "last_name": stringLast name specified on token creation,
          "account": {
            If the connect_token hasn't been used yet, this object will be empty
            "id": stringId of the account created with this token,
            "created": numberUnix timestamp of account creation time,
            "suspended": numberUnix timestamp of account suspension time 0 means not suspended,
            "email_addresses":arrayArray of email addresses for this account. This only lists the actual addresses as strings.,
            "first_name": stringFirst name of account holder,
            "last_name": stringLast name of account holder,
            "sources": arrayList of sources this account gets data from. See sources
            If your key uses 3-legged signatures, the following 2 properties are added
            "access_token": stringOAuth access token to sign all future requests on this account,
            "access_token_secret": stringOAuth access token secret to sign all future requests on this account
          }
        }

        or

        Returns:
            A list of ConnectToken objects.
        """
        if params:
            return self._request_uri('connect_tokens'+'/'+params['token'])
        else:
            return [ConnectToken(self, obj) for obj in self._request_uri('connect_tokens')]

    def post_connect_token(self, **params):
        return ConnectToken(self, self._request_uri("connect_tokens", method="POST", params=params))

    def get_discovery(self, **params):
        """Attempts to discover IMAP settings for a given email address.

        2.0
        Documentation: http://context.io/docs/2.0/discovery

        Lite
        Documentation: http://context.io/lite.0/discovery

        Required Arguments:
            source_type: string - The type of source you want to discover
                settings for. Right now, the only supported source type is IMAP
            email: string - An email address you want to discover IMAP
                settings for. Make sure source_type is set to IMAP.

        Returns:
            A Discovery object.
        """
        if 'source_type' not in params:
            params['source_type'] = 'IMAP'

        all_args = req_args = ['source_type', 'email']

        params = helpers.sanitize_params(params, all_args, req_args)

        return Discovery(self, self._request_uri('discovery', params=params))

    def get_oauth_providers(self):
        """List of oauth providers configured.

        2.0
        Documentation: http://context.io/docs/2.0/oauth_providers#get

        Lite
        Documentation: http://context.io/docs/lite/oauth_providers#get

        Arguments:
            None

        Returns:
            A list of OauthProvider objects.
        """
        return [OauthProvider(self, obj) for obj in self._request_uri('oauth_providers')]

    def post_oauth_provider(self, **params):
        """Add a new OAuth provider.

        Required Arguments:
            type: string -  Identification of the OAuth provider. This must be
                either GMAIL_OAUTH2 and MSLIVECONNECT.
            provider_consumer_key: string - The OAuth consumer key
            provider_consumer_secret: string - The OAuth consumer secret

        Returns:
            a dictionary
        """
        all_args = req_args = ["type", "provider_consumer_key", "provider_consumer_secret"]

        params = helpers.sanitize_params(params, all_args, req_args)

        return self._request_uri("oauth_providers", method="POST", params=params)
