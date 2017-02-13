import mock
import unittest
from contextio.lib.v2_0 import V2_0

from contextio.lib import errors
from contextio.lib.resources.account import Account
from contextio.lib.resources.webhook import WebHook
from contextio.lib.resources.connect_token import ConnectToken
from contextio.lib.resources.discovery import Discovery
from contextio.lib.resources.oauth_provider import OauthProvider

class TestV2_0(unittest.TestCase):
    def setUp(self):
        self.api = V2_0(consumer_key="foo", consumer_secret="bar")

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_accounts_returns_list_of_Account_resources(self, mock_request):
        mock_request.return_value = {"id": "some_id"}
        accounts = self.api.get_accounts()

        self.assertEqual(1, len(accounts))
        self.assertIsInstance(accounts[0], Account)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_account_returns_Account_object(self, mock_request):
        mock_request.return_value = {"id": "some_id"}

        account = self.api.post_account(email="fake@email.com")

        self.assertIsInstance(account, Account)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_connect_tokens_returns_list_of_ConnectToken_resources_without_token(self, mock_request):
        mock_request.return_value = [{"token": "fake_token", "account": {"id": "account_id"}}]

        connect_tokens = self.api.get_connect_tokens()

        self.assertEqual(1, len(connect_tokens))
        self.assertIsInstance(connect_tokens[0], ConnectToken)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_connect_tokens_returns_dictionary_if_token_is_provided(self, mock_request):
        mock_request.return_value = {"token": "fake_token"}

        connect_token = self.api.get_connect_tokens(token="fake_token")

        self.assertEqual({"token": "fake_token"}, connect_token)


    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_connect_token_requires_callback_url(self, mock_request):
        mock_request.return_value = {"token": "fake_token"}

        with self.assertRaises(errors.ArgumentError):
            self.api.post_connect_token()

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_connect_token_returns_ConnectToken(self, mock_request):
        mock_request.return_value = {"token": "fake_token"}

        connect_token_request = self.api.post_connect_token(callback_url="http://some.callback.url")

        self.assertEqual(connect_token_request, {"token": "fake_token"})

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_discovery_returns_discovery_object(self, mock_request):
        mock_request.return_value = {"email": "fake@email.com"}


        discovery = self.api.get_discovery(email="fake@email.com")

        self.assertIsInstance(discovery, Discovery)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_discovery_requires_email_argument(self, mock_request):
        with self.assertRaises(errors.ArgumentError):
            self.api.get_discovery()

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_oauth_providers_returns_list_of_OauthProvider_objects(self, mock_request):
        mock_request.return_value = [{"provider_consumer_key": "1234"}]

        oauth_providers = self.api.get_oauth_providers()

        self.assertEqual(1, len(oauth_providers))
        self.assertIsInstance(oauth_providers[0], OauthProvider)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_oauth_provider_returns_dictionary(self, mock_request):
        mock_request.return_value = {"provider_consumer_key": "123"}

        oauth_provider = self.api.post_oauth_provider(type="VALIDOAUTHTYPE", provider_consumer_key="1234", provider_consumer_secret="1234")

        self.assertEqual({"provider_consumer_key": "123"}, oauth_provider)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_oauth_provider_requires_type_provider_key_and_provider_secret(self, mock_request):
        mock_request.return_value = {"provider_consumer_key": "123"}

        with self.assertRaises(errors.ArgumentError):
            self.api.post_oauth_provider()

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_webhooks_returns_list_of_WebHook_resources(self, mock_request):
        mock_request.return_value = [{"webhook_id": "some_id"}]
        webhooks = self.api.get_webhooks()

        self.assertEqual(1, len(webhooks))
        self.assertIsInstance(webhooks[0], WebHook)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_webhook_returns_success(self, mock_request):
        mock_request.return_value = {"success": "true"}

        webhook = self.api.post_webhook(callback_url="http://callba.ck", failure_notif_url="http://callba.ck")

        self.assertEqual(1, len(webhook))
        self.assertEqual({"success": "true"}, webhook)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_webhook_requires_callback_url(self, mock_request):
        mock_request.return_value = {"success": "false"}

        with self.assertRaises(errors.ArgumentError):
            self.api.post_webhook()
