# -*- coding: utf-8 -*-

from app.api.InterfaceManager.request.request import api_request

class AllTests():

    def __init__(self):
        pass

    def run_case(self, test_cases):

        pass

    def run_interface_case(self, test_cases):
        """

        :param test_cases:
        :return:
        """
        for test_case in test_cases:
            url = test_case.interface_url
            method = test_case.method
            testcase_header = test_case.testcase_header
            testcase_body = test_case.testcase_body
            testcase_verification = test_case.testcase_verification

            api_request.request(method, url, headers=testcase_header, data=testcase_body, testcase_verification=testcase_verification)

