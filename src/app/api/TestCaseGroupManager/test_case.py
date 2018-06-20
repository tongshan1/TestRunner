# -*- coding: utf-8 -*-

from flask import render_template, request

from app import db
from app.api import api
from app.handler import register, success, fail
from app.api.ModuleManager.module import get_all_modules
from module.Testcase import TestInterfacecase
from app.form.test_case_from import TestCaseFrom
from module.System_setting import SystemSetting
from schema.testcase import TestCaseSchema
from flask_wtf.csrf import generate_csrf


@register(api, "/test_case_add.html", methods=["GET", "POST"])
def test_case_add():
    if request.method == 'GET':
        return render_template("test_cases/test_case_add.html", modules=get_all_modules(), csrf_token=generate_csrf(),
                               runner_setting=SystemSetting.get_runner_setting())
    else:
        test_case_from = TestCaseFrom()
        if test_case_from.validate_on_submit():
            test_case = TestInterfacecase(
                interface_url=test_case_from.interface_url.data,
                testcase_name=test_case_from.testcase_name.data,
                module_id=test_case_from.module_id.data,
                testcase_method=test_case_from.testcase_method.data,
                testcase_header=test_case_from.testcase_header.data,
                testcase_body=test_case_from.testcase_body.data,
                is_active=test_case_from.is_active.data,
                testcase_verification=test_case_from.testcase_verification.data
            )
            db.session.add(test_case)
            db.session.commit()
            return success()
        else:
            print(test_case_from.errors)
            return fail(2, error=test_case_from.errors)


@register(api, "/testcase/module/<module_id>")
def get_testcase_by_module(module_id):
    testcases = TestInterfacecase.query.filter(TestInterfacecase.module_id == module_id).all()
    testcases = TestCaseSchema(many=True).dumps(testcases)

    return testcases
