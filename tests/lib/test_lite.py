import mock
import unittest
from contextio.lib.lite import Lite

from contextio.lib import errors
from contextio.lib.resources.user import User
from contextio.lib.resources.webhook import WebHook

class TestLite(unittest.TestCase):
    def setUp(self):
        self.api = Lite(consumer_key="foo", consumer_secret="bar", version="lite")

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_users_returns_a_list_of_User_resources(self, mock_request):
        mock_request.return_value = {"id": "some_id"}
        accounts = self.api.get_users()

        self.assertEqual(1, len(accounts))
        self.assertIsInstance(accounts[0], User)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_user_returns_User(self, mock_request):
        mock_request.return_value = {"id": "some_id"}

        user = self.api.post_user(
            password="fake", email="fake@email.com", server="fake.server", username="fake",
            use_ssl=1, port=993, type="IMAP")

        self.assertIsInstance(user, User)

    def test_post_user_requires_arguments(self):
        with self.assertRaises(errors.ArgumentError):
            self.api.post_connect_token(foo="bar")

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_connect_token_returns_dict(self, mock_request):
        mock_request.return_value = {"token": "fake_token"}

        connect_token_request = self.api.post_connect_token(callback_url="fake.url")

        self.assertEqual(connect_token_request, {"token": "fake_token"})

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
