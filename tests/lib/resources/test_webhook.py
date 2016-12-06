import unittest
from mock import Mock

from contextio.lib.resources.webhook import WebHook


class TestWebHook(unittest.TestCase):
    def test_constructor_creates_message_object_with_all_attributes_in_keys_list(self):
        webhook = WebHook(Mock(), {"webhook_id": "fake_webhook_id"})

        self.assertTrue(hasattr(webhook, "callback_url"))
        self.assertTrue(hasattr(webhook, "failure_notif_url"))
        self.assertTrue(hasattr(webhook, "active"))
        self.assertTrue(hasattr(webhook, "failure"))
        self.assertTrue(hasattr(webhook, "webhook_id"))
        self.assertTrue(hasattr(webhook, "filter_to"))
        self.assertTrue(hasattr(webhook, "filter_from"))
        self.assertTrue(hasattr(webhook, "filter_cc"))
        self.assertTrue(hasattr(webhook, "filter_subject"))
        self.assertTrue(hasattr(webhook, "filter_thread"))
        self.assertTrue(hasattr(webhook, "filter_new_important"))
        self.assertTrue(hasattr(webhook, "filter_file_name"))
        self.assertTrue(hasattr(webhook, "filter_folder_added"))
        self.assertTrue(hasattr(webhook, "filter_folder_removed"))
        self.assertTrue(hasattr(webhook, "filter_to_domain"))
        self.assertTrue(hasattr(webhook, "filter_from_domain"))
        self.assertTrue(hasattr(webhook, "version"))
