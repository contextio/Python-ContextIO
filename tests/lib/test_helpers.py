import unittest
from datetime import datetime

from contextio.lib import helpers
from contextio.lib.errors import ArgumentError


class TestHelpers(unittest.TestCase):
    def test_to_underscore_converts_camel_case_to_undescore_format(self):
        self.assertEqual("this_is_camel_case", helpers.to_underscore("thisIsCamelCase"))

    def test_uncamelize_converts_camel_case_keys_to_underscore_format(self):
        test_dict = {
            "camelCase": "foobar",
            "under_score": "catpants"
        }

        self.assertEqual(
            {"camel_case": "foobar", "under_score": "catpants"},
            helpers.uncamelize(test_dict)
        )

    def test_as_datetime_converts_UNIX_time_to_datetime_object(self):
        self.assertEqual(datetime(2016, 3, 25, 16, 46, 4), helpers.as_datetime(1458942364))

    def test_as_bool_returns_false_if_0_or_False(self):
        self.assertFalse(helpers.as_bool(0))
        self.assertFalse(helpers.as_bool(False))

    def test_as_bool_returns_True_anything_other_than_0_or_False(self):
        self.assertTrue(helpers.as_bool({}))
        self.assertTrue(helpers.as_bool(""))
        self.assertTrue(helpers.as_bool(10))

    def test_sanitize_params_removes_unwanted_params(self):
        allowed_args = ["foo", "dog"]
        params = {
            "foo": "bar",
            "cat": "pants",
            "dog": "shirt"
        }

        self.assertEqual(
            {"foo": "bar", "dog": "shirt"},
            helpers.sanitize_params(params, all_args=allowed_args)
        )

    def test_sanitize_params_throws_error_if_required_param_not_in_params(self):
        allowed_args = ["foo", "dog"]
        params = {
            "foo": "bar",
            "cat": "pants",
            "dog": "shirt"
        }

        with self.assertRaises(ArgumentError):
            helpers.sanitize_params(params, all_args=allowed_args, required_args=["fish"])

    def test_sanitize_params_ignores_params_that_are_set_to_None(self):
        allowed_args = ["foo", "dog"]
        params = {
            "foo": None,
            "dog": "shirt"
        }

        cleaned_params = helpers.sanitize_params(params, all_args=allowed_args)

        self.assertEqual({"dog": "shirt"}, cleaned_params)

    # Not sure if this is being used anywhere - didn't want to remove it in case someone is using
    # this helper directly
    # def test_process_person_info()

    def test_check_for_account_credentials_returns_true_if_password_in_dict(self):
        result = helpers.check_for_account_credentials({"password": "rickjames"})

        self.assertTrue(result)

    def test_check_for_account_credentials_returns_true_if_provider_refresh_token_and_consumer_key_in_dict(self):
        result = helpers.check_for_account_credentials({
            "provider_refresh_token": "han",
            "provider_consumer_key": "shotfirst"
        })

        self.assertTrue(result)

    def test_check_for_account_credentials_raises_ArgumentError_if_no_credentials(self):
        with self.assertRaises(ArgumentError):
            helpers.check_for_account_credentials({})

    def test_check_for_account_credentials_raises_ArgumentError_if_consumer_key_missing(self):
        with self.assertRaises(ArgumentError):
            helpers.check_for_account_credentials({"provider_refresh_token": "han"})

    def test_check_for_account_credentials_raises_ArgumentError_if_refresh_token_missing(self):
        with self.assertRaises(ArgumentError):
            helpers.check_for_account_credentials({"provider_consumer_key": "shotfirst"})

        # if "password" in argument_dict or "provider_refresh_token" in argument_dict and "provider_consumer_key" in argument_dict:
        #     return True
        # else:
        #     raise ArgumentError(
        #         "You must provide either a 'password' or a 'provider_refresh_token'"
        #         " and a 'provider_consumer_key'")
