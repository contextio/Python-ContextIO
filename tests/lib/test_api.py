import json
import mock
import unittest
from rauth import OAuth1Session
from six import PY3

from contextio.lib.api import Api
from contextio.lib.errors import RequestError


class TestApi(unittest.TestCase):
    def setUp(self):
        # some of the following tests mock the OAuth session created in the constructor
        # in for these tests we must redeclare self.api
        self.api = Api(consumer_key="foo", consumer_secret="bar")

    def test_constructor_creates_object_with_default_config(self):
        self.api = Api(consumer_key="foo", consumer_secret="bar")

        self.assertEqual("foo", self.api.consumer_key)
        self.assertEqual("bar", self.api.consumer_secret)
        self.assertEqual("https://api.context.io", self.api.url_base)
        self.assertEqual("2.0", self.api.api_version)
        self.assertEqual(None, self.api.debug)
        self.assertIsInstance(self.api.session, OAuth1Session)

    def test_constructor_creates_object_with_custom_config(self):
        self.api = Api(
            consumer_key="foo",
            consumer_secret="bar",
            url_base="http://fake.url",
            debug="print",
            api_version="lite"
        )

        self.assertEqual("foo", self.api.consumer_key)
        self.assertEqual("bar", self.api.consumer_secret)
        self.assertEqual("http://fake.url", self.api.url_base)
        self.assertEqual("lite", self.api.api_version)
        self.assertEqual("print", self.api.debug)

    def test_constructor_maps_True_to_print_for_debug_value(self):
        self.api = Api(
            consumer_key="foo",
            consumer_secret="bar",
            debug=True
        )

        self.assertEqual("foo", self.api.consumer_key)
        self.assertEqual("bar", self.api.consumer_secret)
        self.assertEqual("print", self.api.debug)

    @mock.patch("contextio.lib.api.six.print_")
    def test_debug_prints_message_when_debug_equals_print(self, mock_six_print):
        self.api = Api(consumer_key="foo", consumer_secret="bar", debug="print")
        mock_response = mock.Mock()
        mock_response.request.url = "fake_url"
        mock_response.request.method = "GET"
        mock_response.status_code = 404

        message = (
            "--------------------------------------------------\n"
            "URL:    {0}\nMETHOD: {1}\nSTATUS: 2\n\nREQUEST\n{3}\n\nRESPON"
            "SE\n{4}\n").format(
                mock_response.request.url, mock_response.request.method, mock_response.status_code,
                mock_response.request.__dict__, mock_response.__dict__)

        self.api._debug(mock_response)

        mock_six_print.assert_called_with(message)

    @mock.patch("contextio.lib.api.logging.debug")
    def test_debug_logs_message_when_debug_equals_log(self, mock_logging_debug):
        self.api = Api(consumer_key="foo", consumer_secret="bar", debug="log")
        mock_response = mock.Mock()
        mock_response.request.url = "fake_url"
        mock_response.request.method = "GET"
        mock_response.status_code = 404
        message = (
            "--------------------------------------------------\n"
            "URL:    {0}\nMETHOD: {1}\nSTATUS: 2\n\nREQUEST\n{3}\n\nRESPON"
            "SE\n{4}\n").format(
                mock_response.request.url, mock_response.request.method, mock_response.status_code,
                mock_response.request.__dict__, mock_response.__dict__)

        self.api._debug(mock_response)

        mock_logging_debug.assert_called_with(message)

    @mock.patch("contextio.lib.api.pkg_resources")
    @mock.patch("contextio.lib.api.OAuth1Session")
    def test_request_defaults_to_GET_method_and_include_user_agent_header(self, mock_session, mock_pkg_resources):
        mock_package = mock.Mock()
        mock_package.version = "v1.0.0"
        mock_pkg_resources.require.return_value = [mock_package]

        mock_session.return_value.request = mock.Mock()
        mock_request = mock_session.return_value.request
        mock_request.return_value = mock.Mock(status_code=400)

        self.api = Api(consumer_key="foo", consumer_secret="bar")

        with self.assertRaises(RequestError):
            self.api._request_uri("catpants")

        mock_request.assert_called_with(
            "GET", "https://api.context.io/2.0/catpants",
            data="",
            header_auth=True,
            headers={'user-agent': 'contextio/2.0/python-lib-v1.0.0'},
            params={}
        )

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_request_uri_raises_RequestError_if_status_not_between_200_and_300(self, mock_request):
        mock_request.side_effect = RequestError

        with self.assertRaises(RequestError):
            self.api._request_uri("catpants")

    @unittest.skipIf(PY3, "Only python2 will implicitly raise UnicodeDecodeError")
    @mock.patch("contextio.lib.api.OAuth1Session")
    def test_request_uri_returns_response_content_if_UnicodeDecodeError_raised(self, mock_session):
        mock_request = mock_session.return_value.request.return_value
        mock_request.json.side_effect = UnicodeDecodeError("", "", 42, 43, "")
        mock_request.status_code = 200
        mock_request.content = bytes("foo bar")

        self.api = Api(consumer_key="foo", consumer_secret="bar")

        response = self.api._request_uri("catpants")

        self.assertEqual("foo bar", response)

    @mock.patch("contextio.lib.api.OAuth1Session")
    def test_request_uri_returns_response_text_if_ValueError_raised(self, mock_session):
        mock_request = mock_session.return_value.request.return_value
        mock_request.status_code = 200
        mock_request.json.side_effect = ValueError()
        mock_request.text = "This is some text"

        self.api = Api(consumer_key="foo", consumer_secret="bar")

        response = self.api._request_uri("catpants")
        self.assertEqual("This is some text", response)

    @mock.patch("contextio.lib.api.Api._request_uri")
    def test_request_uri_returns_json(self, mock_request):
        mock_request.return_value = ({"foo": "bar"})

        response = self.api._request_uri("catpants")

        self.assertEqual({"foo": "bar"}, response)

    @mock.patch("contextio.lib.api.pkg_resources")
    @mock.patch("contextio.lib.api.OAuth1Session")
    def test_request_includes_body_if_method_is_POST(self, mock_session, mock_pkg_resources):
        mock_package = mock.Mock()
        mock_package.version = "v1.0.0"
        mock_pkg_resources.require.return_value = [mock_package]

        mock_request = mock_session.return_value.request
        mock_request.return_value.status_code = 200

        self.api = Api(consumer_key="foo", consumer_secret="bar", api_version="some_version")

        self.api._request_uri("catpants", method="POST", body=json.dumps({"foo": "bar"}))

        mock_request.assert_called_with(
            "POST", "https://api.context.io/some_version/catpants",
            data={"body": '{"foo": "bar"}'},
            header_auth=True,
            headers={'user-agent': 'contextio/some_version/python-lib-v1.0.0'}
        )
