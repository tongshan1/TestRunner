from flask import render_template

from app.handler import register
from app.views import api
from app.module.Report import Report, Result


def filter_result(result):
    """
    :param key:
    :return:
    """
    if result:
        return u"成功"
    else:
        return u"失败"


@register(api, "/report.html", methods=["GET"])
def report_all():
    return render_template("report/index.html", reports=Report.all(), filter_result=filter_result)


@register(api, "/report/<report_id>/detail.html", methods=["GET"])
def report_detail(report_id):
    report = Report.get_by_id(report_id)
    result = Result.get_by_report_id(report_id)

    testcases = []
    for r in result:
        testcase = r.testcase_testgroup.testcase
        testcase_dict = {}
        testcase_dict["result"] = r
        testcase_dict["testcase"] = testcase
        testcases.append(testcase_dict)

    return render_template("report/detail.html", report=report, testcases=testcases)