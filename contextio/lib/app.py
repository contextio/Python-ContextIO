from __future__ import absolute_import

from .api import Api
from .helpers import sanitize_params


class App(Api):
    """Application level endpoints: These apply to both Lite and 2.0 versions. To use application level endpoints, you must instantiate an object using "app" as your API version.
    """
    def get_webhook_logs(self, **params):
        """Webhook logs

        Documentation: https://docs.context.io/#logs

        Optional arguments:
        account: string - Only include logs of webhooks from the specified account id
        webhook_id: string - Only include logs of webhooks from the specified webhook id
        timestamp_before: integer (unix timestamp) - Only include logs of webhooks before a given timestamp.
        timestamp_after: integer (unix timestamp) - Only include logs of webhooks after a given timestamp.
        status_code_from: integer - Only return webhook logs where the status code is greater than the number specified. For example 200)
        status_code_to: integer - Only return webhook logs where the status code is less than the number specified. For example 300)

        Returns: A list of webhook logs
        """

        all_args = ["account", "webhook_id", "timestamp_before", "timestamp_after", "status_code_from", "status_code_to"]
        params = sanitize_params(params, all_args)
        return [obj for obj in self._request_uri("logs/webhooks", params=params)]

    def get_call_logs(self, **params):
        """Call logs

        Documentation: https://docs.context.io/#logs

        Optional arguments:

        account: string - Only include logs of webhooks from the specified account id
        timestamp_before: integer (unix timestamp) - Only include logs of calls before a given timestamp.
        timestamp_after: integer (unix timestamp) - Only include logs of calls after a given timestamp.
        status_code_from: integer - Only return logs of calls where the status code is greater than the number specified. For example 200)
        status_code_to: integer - Only return logs of call where the status code is less than the number specified. For example 500)
        request_method: string - Only return logs of calls where the http method is the one specified. For example, GET
        request_path: string - Only return logs of calls where the request matches this search string. To use regular expressions instead of simple string matching, make sure the string starts and ends with /

        Returns: A list of call logs
        """

        all_args = ["account", "webhook_id", "timestamp_before", "timestamp_after", "status_code_from", "status_code_to", "request_method", "request_path"]
        params = sanitize_params(params, all_args)
        return [obj for obj in self._request_uri("logs/calls", params=params)]

    def post_status_callback_url(self, **params):
        """Post an application level status_callback_url

        Documentation: https://docs.context.io/#status-callback-url

        Required argument:

        status_callback_url: string (URL) - If specified, we'll make a POST request to this URL if the connection status of the email account changes.

        Return: boolean (true / false if operation was successful)
        """

        all_args = req_args = ["status_callback_url"]
        params = sanitize_params(params, all_args, req_args)
        return self._request_uri("status_callback_url", method="POST", params=params)

    def get_status_callback_url(self):
        """Get your application status_callback_url

        Documentation: https://docs.context.io/#status-callback-url

        Arguments: none
        """
        return [obj for obj in self._request_uri("status_callback_url")]

    def delete_status_callback_url(self):
        """Delete your application status_callback_url

        Documentation: https://docs.context.io/#status-callback-url

        Arguments: none
        """
        return self._request_uri("status_callback_url", method="DELETE")
