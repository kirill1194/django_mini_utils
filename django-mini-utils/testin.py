from django.test.utils import override_settings
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.test import APITestCase
import json


@override_settings(DEBUG=True)
class BaseApiTestCase2(APITestCase):
    """Class for testing Rest. To use, you need to create an heir and define a variable of class "api_prefix".
    For each test, use the created class and redefine the "path" """

    path = None
    api_prefix = None

    def buildPath(self, path, **kwargs):
        if not path:
            path = self.path
        assert path is not None, 'You forget to declare a variable "path"'
        assert self.api_prefix is not None, 'You forget to declare a variable "api_prefix"'
        if not self.api_prefix.endswith('/'):
            self.api_prefix += '/'

        if not path.endswith('/'):
            path += '/'

        if len(kwargs) != 0:
            path += '?'
            for key, val in kwargs.items():
                if path[-1] != '/':
                    path += '&{}={}'.format(key, val)
                else:
                    path += '{}={}'.format(key, val)

        return self.api_prefix + path

    @staticmethod
    def dict_to_json(dictionary):
        if dictionary:
            return json.dumps(dictionary)
        else:
            return None

    @staticmethod
    def build_token_headers(token):
        result = dict()
        if token:
            result['HTTP_AUTHORIZATION'] = 'Token {}'.format(token)
        result['content_type'] = "application/json"
        return result

    @staticmethod
    def build_headers(**kwargs):
        headers_row = dict({(k, v) for k, v in kwargs.items() if k.lower().startswith('http')})
        for key in headers_row.keys():
            del kwargs[key]
        headers = dict()
        for k, v in headers_row.items():
            headers[k.upper()] = v
        return headers

    def assertGet(self, data=None, path: str = None, token: str = None, status_code=HTTP_200_OK, **kwargs):
        headers = self.build_headers(kwargs)
        request_path = self.buildPath(path, **kwargs)
        headers.update(self.build_token_headers(token))
        response = self.client.get(request_path, self.dict_to_json(data), **headers)
        self.assertEqual(response.status_code, status_code)
        return response

    def assertPost(self, data=None, path: str = None, token: str = None, status_code=HTTP_201_CREATED, **kwargs):
        headers = self.build_headers(kwargs)
        request_path = self.buildPath(path, **kwargs)
        headers.update(self.build_token_headers(token))

        response = self.client.post(request_path, self.dict_to_json(data), **headers)
        self.assertEqual(response.status_code, status_code)
        return response

    def assertPatch(self, data=None, path: str = None, token: str = None, status_code=HTTP_200_OK, **kwargs):
        headers = self.build_headers(kwargs)
        request_path = self.buildPath(path, **kwargs)
        headers.update(self.build_token_headers(token))

        response = self.client.patch(request_path, self.dict_to_json(data), **headers)
        self.assertEqual(response.status_code, status_code)
        return response

    def assertPut(self, data=None, path: str = None, token: str = None, status_code=HTTP_200_OK, **kwargs):
        headers = self.build_headers(kwargs)
        request_path = self.buildPath(path, **kwargs)
        headers.update(self.build_token_headers(token))

        response = self.client.put(request_path, self.dict_to_json(data), **headers)
        self.assertEqual(response.status_code, status_code)
        return response

    def assertDelete(self, data=None, path: str = None, token: str = None, status_code=HTTP_204_NO_CONTENT,
                     **kwargs):
        headers = self.build_headers(kwargs)
        request_path = self.buildPath(path, **kwargs)
        headers.update(self.build_token_headers(token))

        response = self.client.delete(request_path, self.dict_to_json(data), **headers)
        self.assertEqual(response.status_code, status_code)
        return response
