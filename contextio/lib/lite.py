from __future__ import absolute_import

from .helpers import sanitize_params, check_for_account_credentials
from .resources.user import User
from .resources.webhook import WebHook

from .api import Api

class Lite(Api):
    def get_users(self, **kwargs):
        all_args = ["email", "status", "status_ok", "limit", "offset"]

        params = sanitize_params(kwargs, all_args)
        return [User(self, obj) for obj in self._request_uri("users", params=params)]

    def post_user(self, **kwargs):
        req_args = ["email", "server", "username", "use_ssl", "port", "type"]

        if check_for_account_credentials(kwargs):
            all_args = [
                "password", "provider_refresh_token", "provider_consumer_key", "migrate_account_id",
                "first_name", "last_name"
            ] + req_args

            params = sanitize_params(kwargs, all_args, req_args)

            return User(self, self._request_uri("users", method="POST", params=params))


    def post_connect_token(self, **kwargs):
        req_args = ["callback_url"]
        all_args = ["email", "first_name", "last_name", "status_callback_url"] + req_args

        params = sanitize_params(kwargs, all_args, req_args)

        return super(Lite, self).post_connect_token(**params)

    def get_webhooks(self):
        return [WebHook(self, obj) for obj in self._request_uri("webhooks")]

    def post_webhook(self, **kwargs):
        req_args = ["callback_url", "failure_notif_url"]
        all_args = ["callback_url", "failure_notif_url", "filter_to", "filter_from", "filter_cc",
            "filter_subject", "filter_thread", "filter_new_important",
            "filter_file_name", "filter_folder_added",
            "filter_to_domain", "filter_from_domain", "receive_all_changes", "receive_historical", "include_body", "body_type",  "active"
        ]

        params = sanitize_params(kwargs, all_args, req_args)

        return self._request_uri("webhooks", method="POST", params=params)
