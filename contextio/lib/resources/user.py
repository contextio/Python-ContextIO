from __future__ import absolute_import

from ..helpers import sanitize_params, check_for_account_credentials
from .base_resource import BaseResource
from .connect_token import ConnectToken
from .email_account import EmailAccount
from .webhook import WebHook


class User(BaseResource):
    resource_id = "id"
    keys = [
        "id", "email_accounts", "email_addresses", "created", "first_name", "last_name",
        "resource_url"
    ]

    def __init__(self, parent, definition):
        super(User, self).__init__(parent, "users/{id}", definition)

    def post(self, **kwargs):
        all_args = ["first_name", "last_name"]

        for prop in all_args:
            value = kwargs.get(prop)
            if value:
                setattr(self, prop, value)

        return super(User, self).post(params=kwargs, all_args=all_args)

    def delete(self):
        return super(User, self).delete()

    def get_connect_tokens(self):
        return [ConnectToken(self, obj) for obj in self._request_uri("connect_tokens")]

    def post_connect_token(self, **params):
        req_args = ["callback_url"]
        all_args = [
            "email", "first_name", "last_name", "source_callback_url",
            "source_sync_all_folders", "source_sync_flags", "source_raw_file_list",
            "status_callback_url"
        ] + req_args

        return super(User, self).post(
            uri="connect_tokens", return_bool=False, params=params, all_args=all_args,
            required_args=req_args)

    def get_email_accounts(self, **params):
        all_args = ["status", "status_ok"]

        params = sanitize_params(params, all_args)

        return [EmailAccount(self, obj) for obj in self._request_uri("email_accounts", params=params)]

    def post_email_account(self, **kwargs):
        req_args = ["email", "server", "username", "use_ssl", "port", "type"]

        all_args = req_args + ["status_callback_url"]

        email_account = super(User, self).post(
            uri="email_accounts", params=kwargs, return_bool=False, all_args=all_args,
            required_args=req_args
        )

        if bool(email_account["success"]) is False:
            return False

        return EmailAccount(self, email_account)

        if check_for_account_credentials(kwargs):
            all_args = ["migrate_account_id", "first_name", "last_name"] + req_args
            params = sanitize_params(kwargs, all_args, req_args)

            return User(self, self._request_uri("users", method="POST", params=params))

    def get_webhooks(self):
        return [WebHook(self, obj) for obj in self._request_uri("webhooks")]

    def post_webhook(self, **kwargs):
        req_args = ["callback_url", "failure_notif_url"]

        all_args = req_args + [
            "filter_to", "filter_from",
            "filter_cc", "filter_subject", "filter_thread",
            "filter_new_important", "filter_file_name", "filter_folder_added",
            "filter_folder_removed", "filter_to_domain", "filter_from_domain",
            "include_body", "body_type"
        ]

        webhook = super(User, self).post(
            uri="webhooks", params=kwargs, return_bool=False, all_args=all_args,
            required_args=req_args
        )

        if bool(webhook["success"]) is False:
            return False

        return WebHook(self, webhook)
