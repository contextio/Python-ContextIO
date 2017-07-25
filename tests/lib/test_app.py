from __future__ import print_function
import mock
import unittest

from contextio.lib import errors
from contextio.lib.app import App

class TestApp(unittest.TestCase):
    def setUpApp(self):
        self.api = App(consumer_key="foo", consumer_secret="bar", version="app")

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_webhook_logs(self, mock_request):
        self.setUpApp()

        mock_request.return_value = [{"webhook_id": "some_id"}]

        webhook_logs = self.api.get_webhook_logs()

        self.assertEqual(1,len(webhook_logs))
        self.assertDictEqual({"webhook_id": "some_id"}, webhook_logs[0])

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_call_logs(self, mock_request):
        self.setUpApp()

        mock_request.return_value = [{"http_return_code": "code"}]

        call_logs = self.api.get_call_logs()

        self.assertEqual(1,len(call_logs))
        self.assertDictEqual({"http_return_code": "code"}, call_logs[0])


    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_post_status_callback_url(self, mock_request):
        self.setUpApp()

        mock_request.return_value = [{"success": "true"}]

        response = self.api.post_status_callback_url(status_callback_url="http://callba.ck")

        self.assertEqual(1,len(response))
        self.assertDictEqual({"success": "true"}, response[0])

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_get_status_callback_url(self, mock_request):
        self.setUpApp()

        mock_request.return_value = [{"status_callback_url": "http://callba.ck"}]

        response = self.api.get_status_callback_url()

        self.assertEqual(1,len(response))
        self.assertDictEqual({"status_callback_url": "http://callba.ck"}, response[0])

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_delete_status_callback_url(self, mock_request):
        self.setUpApp()

        mock_request.return_value = [{"success": "true"}]

        response = self.api.delete_status_callback_url()

        self.assertEqual(1,len(response))
        self.assertDictEqual({"success": "true"}, response[0])
