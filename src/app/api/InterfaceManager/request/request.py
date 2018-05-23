# -*- coding: utf-8 -*-
import requests
from requests.exceptions import (InvalidSchema, InvalidURL, MissingSchema,)
from .util import replace_variable, str_to_dict
from .response import ApiResponse


class ApiRequest(object):

    session = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        cls.session = requests.session()
        return object.__new__(cls, *args, **kwargs)

    def request(self, method, path, **kwargs):
        """
        请求api
        :param path:
        :param method:
        :param kwargs:
        :return:
        """

        method, path, kwargs = self.__init_request(method, path, **kwargs)
        if "headers" in kwargs.keys() and kwargs["headers"].get("Content-type") == "JSON(application/json)":

            response = self._send_request_safe_mode(method, path, json=kwargs["data"])
        else:
            response = self._send_request_safe_mode(method, path, data=kwargs["data"])

        api_response = ApiResponse(response)

        if kwargs.get("testcase_verification"):
            result = api_response.validate(kwargs["testcase_verification"])

        return response.text

    def __init_request(self, method, path, **kwargs):
        """
        替换变量
        :return:
        """
        # 替换path
        path = replace_variable(path)

        for key, value in kwargs.items():
            if value in [None,  "", {}]:
                del kwargs[key]
            else:
                kwargs[key] = str_to_dict(replace_variable(value))

        return method, path, kwargs

    def _send_request_safe_mode(self, method, url, **kwargs):
        """
        Send a HTTP request, and catch any exception that might occur due to connection problems.
        Safe mode has been removed from requests 1.x.
        """
        try:

            return self.session.request(method, url, **kwargs)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise

api_request = ApiRequest()