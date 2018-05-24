# -*- coding: utf-8 -*-

from app.api.InterfaceManager.request.request import api_request
from app.api.TestCaseGroupManager.util import get_testcase_by_group_id
from module.Report import Result, Report
from app import db


class AllTests():

    def __init__(self):
        pass

    def run_case(self, test_group_id):

        self.run_interface_case(test_group_id)

    def run_interface_case(self, test_group_id):
        """
        运行一次新建一个report
                1 pass
                 2 error
                 3 fail
        :param test_group_id:
        :return:
        """
        test_cases = get_testcase_by_group_id(test_group_id)
        report = Report(testgroup_id=test_group_id)
        total = 0
        success = 0
        fail = 0
        error = 0
        report_result = True
        db.session.add(report)
        db.session.commit()

        for testcase_testgroup_id, test_case in test_cases.items():
            total +=1
            url = test_case.interface_url
            method = test_case.testcase_method
            testcase_header = test_case.testcase_header
            testcase_body = test_case.testcase_body
            testcase_verification = test_case.testcase_verification

            response, result_one = api_request.request(method, url, headers=testcase_header, data=testcase_body, testcase_verification=testcase_verification)
            result = Result(report.id, testcase_testgroup_id, result_one.result, result_one.note)
            db.session.add(result)

            if result_one.result == 1:
                # 通过的用例
                success += 1
            if result_one.result == 2:
                report_result = False
                error +=1
            if result_one.result == 3:
                report_result = False
                fail += 1

        report.total = total
        report.success = success
        report.fail = fail
        report.error = error
        report.result = report_result

        db.session.add(report)
        db.session.commit()