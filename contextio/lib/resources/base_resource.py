from __future__ import absolute_import

from .. import helpers
from ..errors import MissingResourceId
import functools
import logging
import six

if six.PY2:
    from urllib import quote
else:
    from urllib.parse import quote

no_resource_id_required = ["BaseResource", "Discovery"]


def only(*versions):
    def _only(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.api_version not in list(versions):
                raise Exception(
                    "`{0}()` is not implemented for the {1} version of the api".format(
                        method.__name__, self.api_version))
            return method(self, *args, **kwargs)
        return wrapper
    return _only


class BaseResource(object):
    """Base class for resource objects."""
    keys = []

    def __init__(self, parent, base_uri, definition):
        class_name = self.__class__.__name__
        if class_name not in no_resource_id_required and self.resource_id not in definition:
            raise MissingResourceId(
                "Resource {0} requires attribute '{1}' for initialization".format(
                    self.__class__.__name__, self.resource_id))

        if definition == "":
            logging.error('Empty response received for ' + base_uri + "")
            return

        try:
            definition = helpers.uncamelize(definition)
        except:
            logging.error('Invalid response received for ' + base_uri + "")
            return

        self.parent = parent

        self.api_version = parent.api_version if hasattr(parent, "api_version") else "2.0"

        self._set_instance_attributes(parent, definition)

        unidict = {six.text_type(k): six.text_type(v) for k, v in definition.items()}
        self.base_uri = quote(base_uri.format(**unidict))

    def _set_instance_attributes(self, parent, definition):
        if isinstance(self.__class__.keys, dict):
            keys = self.__class__.keys[self.api_version]
        else:
            keys = self.__class__.keys

        for k in keys:
            if k in definition:
                setattr(self, k, definition[k])
            else:
                setattr(self, k, None)

    def _uri_for(self, *elems):
        """Joins API endpoint elements and returns a string."""
        return '/'.join([self.base_uri] + list(elems))

    def _request_uri(self, uri_endpoint="", method="GET", params={}, headers={}, body=''):
        """Gathers up request elements and helps form the request object.

        Required Arguments:
            uri_endpoint: string - the endpoint.

        Optional Arguments:
            method: string - the method of the request. Possible values are
                'GET', 'POST', 'DELETE', 'PUT'
            params: dict - parameters to pass along
            headers: dict - any specific http headers
            body: string - request body, only used on a few PUT statements
        """
        uri = self._uri_for(uri_endpoint)
        return self.parent._request_uri(
            uri, method=method, params=params, headers=headers, body=body)

    def get(self, uri="", return_bool=True, params={}, all_args=[], required_args=[]):
        response = self._request_uri(uri, params=helpers.sanitize_params(params, all_args, required_args))
        self.__init__(self.parent, response)

        if return_bool:
            return True

        return response

    def delete(self, uri=""):
        response = self._request_uri(uri, method='DELETE')
        return bool(response.get('success', False))

    def post(self, uri="", return_bool=True, params={}, headers={}, all_args=[], required_args=[]):
        params = helpers.sanitize_params(params, all_args, required_args)
        response = self._request_uri(uri, method="POST", params=params, headers=headers)

        if return_bool is True:
            if 'success' in response:
                return bool(response.get('success', False))
            if 'status' in response:
                return True if response.get('status') == 'OK' else False

            return False

        return response

    def put(self):
        logging.info("This method is not implemented")
