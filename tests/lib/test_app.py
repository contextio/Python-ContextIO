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

