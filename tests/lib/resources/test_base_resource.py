from mock import Mock, patch
import unittest

from contextio.lib.errors import MissingResourceId
from contextio.lib.resources.base_resource import BaseResource


class MockResource(BaseResource):
    resource_id = "id"
    keys = ["id", "foo", "baz"]

    def __init__(self, parent, definition):
        super(MockResource, self).__init__(parent, "test/{id}", definition)


class TestBaseResource(unittest.TestCase):
    @patch("contextio.lib.resources.base_resource.logging.error")
    def test_constructor_logs_error_if_definition_is_empty_string(self, mock_logging_error):
        BaseResource(Mock(spec=[]), "/some-uri", "")

        mock_logging_error.assert_called_with("Empty response received for /some-uri")

    @patch("contextio.lib.resources.base_resource.helpers.uncamelize")
    @patch("contextio.lib.resources.base_resource.logging.error")
    def test_constructor_logs_error_if_unable_to_unacamelize_definition(self, mock_logging_error, mock_uncamelize):
        mock_uncamelize.side_effect = Exception
        BaseResource(Mock(), "/some-uri", {"foo": "bar"})

        mock_logging_error.assert_called_with("Invalid response received for /some-uri")

    def test_constructor_sets_attributes_defined_in_class_keys_list(self):
        mock_parent = Mock()
        mock_parent.api_version = "some_version"
        mock_resource = MockResource(mock_parent, {"id": "fake_id", "foo": "bar"})

        self.assertEqual("fake_id", mock_resource.id)
        self.assertEqual("some_version", mock_resource.api_version)
        self.assertEqual("bar", mock_resource.foo)
        self.assertIsNone(mock_resource.baz)
        self.assertEqual(mock_parent, mock_resource.parent)
        self.assertEqual("test/fake_id", mock_resource.base_uri)

    def test_constructor_sets_attributes_defined_in_class_keys_dict(self):
        mock_parent = Mock()
        mock_parent.api_version = "some_version"

        class MockResource(BaseResource):
            resource_id = "id"
            keys = {
                "some_version": ["id", "foo", "baz"]
            }

            def __init__(self, parent, definition):
                super(MockResource, self).__init__(parent, "test/{id}", definition)

        mock_resource = MockResource(mock_parent, {"id": "fake_id", "foo": "bar"})

        self.assertEqual("fake_id", mock_resource.id)
        self.assertEqual("some_version", mock_resource.api_version)
        self.assertEqual("bar", mock_resource.foo)
        self.assertIsNone(mock_resource.baz)
        self.assertEqual(mock_parent, mock_resource.parent)
        self.assertEqual("test/fake_id", mock_resource.base_uri)

    def test_constructor_raises_error_if_resource_id_not_in_definition(self):
        mock_parent = Mock()
        with self.assertRaises(MissingResourceId):
            MockResource(mock_parent, {"foo": "bar"})

    def test_constructor_default_api_version_to_2_0(self):
        class MockParent(object):
            pass

        mock_resource = MockResource(MockParent, {"id": "bar"})

        self.assertEqual("2.0", mock_resource.api_version)

    def test_uri_for_joins_arguments_with_base_uri(self):
        base_resource = BaseResource(Mock(), "test/{id}", {"id": "fake_id"})
        uri = base_resource._uri_for('some','other-resource')

        self.assertEqual("test/fake_id/some/other-resource", uri)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_get_calls_init_on_itself_with_its_parent_object_and_request_result_as_arguments(self, mock_request):
        mock_parent = Mock()
        mock_request.return_value = {"id": "fake_id", "foo": "catpants"}
        mock_resource = MockResource(mock_parent, {"id": "fake_id", "foo": "bar"})

        self.assertEqual("bar", mock_resource.foo)
        response = mock_resource.get()

        self.assertEqual("catpants", mock_resource.foo)
        self.assertEqual(mock_parent, mock_resource.parent)
        self.assertEqual(True, response)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_get_returns_bool_by_default(self, mock_request):
        mock_parent = Mock()
        mock_request.return_value = {"id": "fake_id", "foo": "catpants"}
        mock_resource = MockResource(mock_parent, {"id": "fake_id", "foo": "bar"})

        response = mock_resource.get()

        self.assertEqual(True, response)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_get_returns_body_of_response_if_return_bool_False(self, mock_request):
        mock_parent = Mock()
        mock_request.return_value = {"id": "fake_id", "foo": "catpants"}
        mock_resource = MockResource(mock_parent, {"id": "fake_id", "foo": "bar"})

        response = mock_resource.get(return_bool=False)

        self.assertEqual({"id": "fake_id", "foo": "catpants"}, response)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_delete_sends_delete_request_to_resource_base_uri(self, mock_request):
        base_resource = BaseResource(Mock(), "test/{id}", {"id": "fake_id"})
        base_resource.delete()

        mock_request.assert_called_with('', method="DELETE")

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_delete_returns_boolean(self, mock_request):
        mock_request.return_value = {"success": True}
        base_resource = BaseResource(Mock(), "test/{id}", {"id": "fake_id"})
        response = base_resource.delete()

        self.assertTrue(response)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_post_returns_boolean_by_default(self, mock_request):
        mock_request.return_value = {"success": True}
        base_resource = BaseResource(Mock(), "test/{id}", {"id": "fake_id"})
        response = base_resource.post()

        self.assertTrue(response)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_post_returns_false_if_success_not_in_response(self, mock_request):
        mock_request.return_value = {"nope": True}
        base_resource = BaseResource(Mock(), "test/{id}", {"id": "fake_id"})
        response = base_resource.post()

        self.assertFalse(response)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_post_returns_false_if_success_is_false(self, mock_request):
        mock_request.return_value = {"nope": False}
        base_resource = BaseResource(Mock(), "test/{id}", {"id": "fake_id"})
        response = base_resource.post()

        self.assertFalse(response)

    @patch("contextio.lib.resources.base_resource.BaseResource._request_uri")
    def test_post_returns_body_of_response_if_return_bool_False(self, mock_request):
        mock_request.return_value = {"success": True}
        base_resource = BaseResource(Mock(), "test/{id}", {"id": "fake_id"})
        response = base_resource.post(return_bool=False)

        self.assertEqual({"success": True}, response)
