# -*- coding: utf-8 -*-

from flask import render_template, request

from app import db
from app.api import api
from app.handler import register, success, fail
from module.Testcase import TestInterfacecase
from module.System_setting import SystemSetting
from module.Interface import Interface
from app.form.test_case_from import TestInterfaceCaseFrom, populate_interface_testcase, populate_interface
from schema.testcase import TestCaseSchema
from app.api.InterfaceManager.request.request import api_request
from app.logger import logger


def init_field_data(field):
    data = {}
    for v in field:
        key = v.get("key")
        value = v.get("value")
        data[key] = value
    return data


def init_verification_data(verification):
    data = {}
    for v in verification:
        i = []
        key = v.get("key")
        i.append(v.get("value"))
        i.append(v.get("save"))
        i.append(v.get("v_type"))
        data[key] = i
    return data


@register(api, "/test_case_add.html", methods=["GET", "POST"])
def test_case_add():
    interface_id = request.args.get("interface_id")
    form = TestInterfaceCaseFrom()
    if interface_id:
        interface_obj = Interface.get_by_id(interface_id)
        form = populate_interface(interface_obj)
    if request.method == 'GET':
        return render_template("test_cases/test_case.html", form=form, runner_setting=SystemSetting.get_runner_setting(), title=u"添加")
    else:
        form = TestInterfaceCaseFrom(request.form)

        data_type = request.form.get("data_type")

        if form.validate():
            test_case_obj = TestInterfacecase()
            test_case_obj.interface_url= form.interface_url.data
            test_case_obj.testcase_name = form.testcase_name.data
            test_case_obj.testcase_method = form.testcase_method.data
            test_case_obj.module = form.module.data
            test_case_obj.testcase_header = init_field_data(form.testcase_header.data)
            test_case_obj.testcase_query = init_field_data(form.testcase_query.data)
            if (data_type == "JSON_data_select"):
                test_case_body = form.testcase_json.data
            else:
                test_case_body = init_field_data(form.testcase_data.data)
            test_case_obj.testcase_body = test_case_body
            test_case_obj.testcase_verification = init_verification_data(form.testcase_verification.data)
            db.session.add(test_case_obj)
            db.session.commit()
            return success()
        else:
            logger.error(form.errors)
            return fail(2, error=form.errors)


@register(api, "/test_case_list.html", methods=["GET", "POST"])
def test_case_list():
    testcases = TestInterfacecase.get_all()
    return render_template("test_cases/test_case_list.html", testcases=testcases)


@register(api, "/testcase/run", methods=["POST"])
def testcase_request():

    data_type = request.form.get("data_type")
    runner_setting = request.form.get("runner_setting")
    form = TestInterfaceCaseFrom(request.form)

    if(data_type == "JSON_data_select"):
        test_case_body = form.testcase_json.data
    else:
        test_case_body = init_field_data(form.testcase_data.data)

    interface_url = form.interface_url.data
    testcase_method = form.testcase_method.data
    testcase_header = init_field_data(form.testcase_header.data)
    testcase_query = init_field_data(form.testcase_query.data)
    testcase_verification = init_verification_data(form.testcase_verification.data)

    response, result = api_request.request(testcase_method, interface_url, headers=testcase_header,
                                           data=test_case_body, testcase_verification=testcase_verification,
                                           params=testcase_query, runner_setting=runner_setting)

    return response


@register(api, "/testcase/<testcase_id>/test_case_edit.html", methods=["GET", "POST"])
def testcase_edit(testcase_id):
    test_case_obj = TestInterfacecase.get_by_id(testcase_id)
    if request.method == "GET":
        form = populate_interface_testcase(test_case_obj)
        return render_template("test_cases/test_case.html", form=form,
                               runner_setting=SystemSetting.get_runner_setting(), title=u"编辑")
    else:
        form = TestInterfaceCaseFrom(request.form)
        data_type = request.form.get("data_type")

        if form.validate():
            test_case_obj.interface_url = form.interface_url.data
            test_case_obj.testcase_name = form.testcase_name.data
            test_case_obj.testcase_method = form.testcase_method.data
            test_case_obj.module = form.module.data
            test_case_obj.testcase_header = init_field_data(form.testcase_header.data)
            test_case_obj.testcase_query = init_field_data(form.testcase_query.data)
            if (data_type == "JSON_data_select"):
                test_case_body = form.testcase_json.data
            else:
                test_case_body = init_field_data(form.testcase_data.data)
            test_case_obj.testcase_body = test_case_body
            test_case_obj.testcase_verification = init_verification_data(form.testcase_verification.data)
            db.session.add(test_case_obj)
            db.session.commit()
            return success()
        else:
            logger.error(form.errors)
            return fail(2, error=form.errors)


@register(api, "/testcase/module/<module_id>")
def get_testcase_by_module(module_id):
    testcases = TestInterfacecase.query.filter(TestInterfacecase.module_id == module_id).all()
    testcases = TestCaseSchema(many=True).dumps(testcases)

    return testcases
