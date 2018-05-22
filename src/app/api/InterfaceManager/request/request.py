# -*- coding: utf-8 -*-
import requests
from requests.exceptions import (InvalidSchema, InvalidURL, MissingSchema,)
from .util import replace_variable, set_variable, str_to_dict


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

        method, path, kwargs = self.__init_request(method, path, kwargs)
        if "headers" in kwargs.keys() and kwargs["headers"].get("Content-type") == "JSON(application/json)":

            response = self._send_request_safe_mode(method, path, json=kwargs["data"])
        else:
            response = self._send_request_safe_mode(method, path, data=kwargs["data"])

        return response.text

    def __init_request(self, method, path, **kwargs):
        """
        替换变量
        :return:
        """
        # 替换path
        path = replace_variable(path)

        if "headers" in kwargs.keys():
            kwargs["headers"] = str_to_dict(replace_variable(kwargs["headers"]))

        if "data" in kwargs.keys():
            kwargs["data"] = str_to_dict(replace_variable(kwargs["data"]))

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