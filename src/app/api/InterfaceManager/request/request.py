# -*- coding: utf-8 -*-
import requests
from requests.exceptions import (InvalidSchema, InvalidURL, MissingSchema,)
from .util import replace_variable, str_to_dict
from .response import ApiResponse, DictObj


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
        result_one = DictObj()
        note = ""
        response = ""
        testcase_verification = ""
        try:

            method, path, kwargs = self.__init_request(method, path, **kwargs)

            if "testcase_verification" in kwargs.keys():
                testcase_verification = kwargs.pop("testcase_verification")

            if "headers" in kwargs.keys() and kwargs["headers"].get("Content-type") == "application/json":

                response = self._send_request_safe_mode(method, path, json=kwargs["data"])
            else:

                response = self._send_request_safe_mode(method, path, **kwargs)

            api_response = ApiResponse(response)
            response = response.text

            if testcase_verification != "":
                result = api_response.validate(testcase_verification)
            else:
                result = 1

            result_one.result = result
            result_one.note = note
        except Exception as e:

            result_one.result = 2
            result_one.note = str(e)
        finally:
            return response, result_one

    def __init_request(self, method, path, **kwargs):
        """
        替换变量
        :return:
        """
        # 替换path
        path = replace_variable(path)
        print(kwargs)
        for key in list(kwargs.keys()):
            if kwargs[key] in [None,  "", {}, '{"":""}', '{}']:
                kwargs.pop(key)
            else:
                kwargs[key] = str_to_dict(replace_variable(kwargs[key]))

        return method, path, kwargs

    def _send_request_safe_mode(self, method, url, **kwargs):
        """
        Send a HTTP request, and catch any exception that might occur due to connection problems.
        Safe mode has been removed from requests 1.x.
        """

        return self.session.request(method, url, **kwargs)
        # try:
        #
        #     return self.session.request(method, url, **kwargs)
        # except (MissingSchema, InvalidSchema, InvalidURL) as e:
        #     print(e)

api_request = ApiRequest()