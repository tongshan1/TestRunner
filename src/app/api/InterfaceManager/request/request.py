# -*- coding: utf-8 -*-
import requests
from requests.exceptions import (InvalidSchema, InvalidURL, MissingSchema,)
from .util import replace_variable, str_to_dict
from .response import ApiResponse, DictObj
from app import logger


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
        testcase_verification = {}

        # method, path, kwargs = self.__init_request(method, path, **kwargs)
        #
        # if "testcase_verification" in kwargs.keys():
        #     testcase_verification = kwargs.pop("testcase_verification")
        #
        # if "headers" in kwargs.keys() and kwargs["headers"].get("Content-type") == "application/json":
        #
        #     json = kwargs.pop("data", None)
        #     response = self._send_request_safe_mode(method, path, json=json, **kwargs)
        # else:
        #
        #     response = self._send_request_safe_mode(method, path, **kwargs)
        #
        # api_response = ApiResponse(response)
        # response = response.text
        # logger.debug("get response" + response)
        # if testcase_verification != {}:
        #     logger.error(testcase_verification)
        #     result = api_response.validate(testcase_verification)
        # else:
        #     result = 1
        #
        # result_one.result = result
        # result_one.note = note
        #
        # return response, result_one

        try:
            method, path, kwargs = self.__init_request(method, path, **kwargs)

            if "testcase_verification" in kwargs.keys():
                testcase_verification = kwargs.pop("testcase_verification")

            if "headers" in kwargs.keys() and kwargs["headers"].get("Content-type") == "application/json":

                json = kwargs.pop("data", None)
                response = self._send_request_safe_mode(method, path, json=json, **kwargs)
            else:

                response = self._send_request_safe_mode(method, path, **kwargs)

            api_response = ApiResponse(response)
            response = response.text
            logger.debug("get response" + response)
            if testcase_verification != "":
                result = api_response.validate(testcase_verification)
            else:
                result = 1

            result_one.result = result
            result_one.note = response
        except Exception as e:

            logger.error(e)

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
        logger.debug("request kwargs"+str(kwargs))

        # 获取运行环境 替换变量
        runner_setting = kwargs.pop("runner_setting", "")

        path = replace_variable(runner_setting, path)

        for key in list(kwargs.keys()):
            if kwargs[key] in [None,  "", {}, '{"":""}', '{}']:
                kwargs.pop(key)
            else:
                kwargs[key] = str_to_dict(replace_variable(runner_setting, kwargs[key]))

        return method, path, kwargs

    def _send_request_safe_mode(self, method, url, **kwargs):
        """
        Send a HTTP request, and catch any exception that might occur due to connection problems.
        Safe mode has been removed from requests 1.x.
        """
        logger.debug("send with kwargs: ================")
        logger.debug(kwargs)
        logger.debug("==================================")

        return self.session.request(method, url, **kwargs)
        # try:
        #
        #     return self.session.request(method, url, **kwargs)
        # except (MissingSchema, InvalidSchema, InvalidURL) as e:
        #     logger.error(e)
        #     return e

api_request = ApiRequest()