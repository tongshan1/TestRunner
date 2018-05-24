from flask import request, redirect, render_template
from app.handler import register, success, fail
from app.api import api
from module.Report import Report, Result


@register(api, "/report.html", methods=["GET"])
def report_all():
    return render_template("report/report_list.html", reports=Report.all())


@register(api, "/report/<report_id>/report_detail.html", methods=["GET"])
def report_detail(report_id):
    report = Report.get_by_id(report_id)
    result = Result.get_by_report_id(report_id)

    for r in result:
        testcase = r.testcase_testgroup.testcase


    return render_template("report/report_detail.html", report=report)