import json

from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, FieldList, FormField, SelectField
from wtforms_alchemy.fields import QuerySelectField
from wtforms.validators import length, data_required
from module.Module import Module
from app.logger import logger


class TestCaseFrom(Form):
    interface_url = StringField('interface_url', [length(min=0), data_required(message=u'接口url不能为空')])
    testcase_name = StringField('testcase_name', [data_required(message=u'接口名不能为空')])
    module_id = IntegerField("module_id", [data_required(message=u'所属某块不能为空')])
    testcase_method = StringField('testcase_method',
                                  [length(min=0, max=100), data_required(message=u'testcase_method不能为空')])
    testcase_header = StringField('testcase_header')
    testcase_body = StringField('testcase_body')
    testcase_verification = StringField('testcase_verification')
    is_active = BooleanField('is_active')

Method = {
    "GET": "GET",
    "POST": "POST",
    "PUT": "PUT",
    "DELETE": "DELETE",
    "PATCH": "PATCH",
    "HEAD": "HEAD",
    "OPTIONS": "OPTIONS"
}


class HeaderForm(Form):
    meta = {'csrf': False}
    key = StringField(u'变量名')
    value = StringField(u'变量值')


class BodyForm(Form):
    meta = {'csrf': False}
    key = StringField(u'变量名')
    value = StringField(u'变量值')


class QueryForm(Form):
    meta = {'csrf': False}
    key = StringField(u'变量名')
    value = StringField(u'变量值')


class VerificationForm(Form):
    meta = {'csrf': False}
    key = StringField(u'变量名')
    value = StringField(u'变量值')
    save = BooleanField(u"保存")


def get_all_module():
    return Module.get_all()


def get_method():
    method = [(key, value) for key, value in Method.items()]
    return method


def str_to_dict(str):
    try:

        return json.loads(str)
    except ValueError:
        return {}
    except TypeError:
        return {}


class TestInterfaceCaseFrom(Form):
    testcase_body_type = ""
    interface_url = StringField(u'接口url', [length(min=0), data_required(message=u'接口url不能为空')])
    testcase_name = StringField(u'接口名称', [data_required(message=u'接口名不能为空')])
    module = QuerySelectField(u"所属模块", query_factory=get_all_module)
    testcase_method = SelectField(u"接口方法", choices=get_method())
    testcase_header = FieldList(FormField(HeaderForm), min_entries=1)
    testcase_query = FieldList(FormField(QueryForm), min_entries=1)
    testcase_body = FieldList(FormField(BodyForm), min_entries=1)
    testcase_verification = FieldList(FormField(VerificationForm), min_entries=1)


def populate_interface_testcase(interface_testcase_obj):
    form = TestInterfaceCaseFrom()
    form.interface_url.data = interface_testcase_obj.interface_url
    form.testcase_name.data = interface_testcase_obj.testcase_name
    form.module.data = interface_testcase_obj.module
    form.testcase_method.data = interface_testcase_obj.testcase_method

    while len(form.testcase_header) > 0:
        form.testcase_header.pop_entry()

    while len(form.testcase_query) > 0:
        form.testcase_query.pop_entry()

    while len(form.testcase_body) > 0:
        form.testcase_body.pop_entry()

    while len(form.testcase_verification) > 0:
        form.testcase_verification.pop_entry()

    testcase_header = str_to_dict(interface_testcase_obj.testcase_header)

    for k, v in testcase_header.items():
        header_form = HeaderForm()
        header_form.key = k
        header_form.value = v

        if k == "Content-type":
            form.testcase_header_type = v

        form.testcase_header.append_entry(header_form)

    if not testcase_header:
        form.testcase_header.append_entry()

    testcase_query = str_to_dict(interface_testcase_obj.testcase_query)
    for k, v in testcase_query.items():
        query_form = QueryForm()
        query_form.key = k
        query_form.value = v

        form.testcase_query.append_entry(query_form)

    if not testcase_query:
        form.testcase_query.append_entry()

    testcase_body = str_to_dict(interface_testcase_obj.testcase_body)
    for k, v in testcase_body.items():
        body_form = BodyForm()
        body_form.key = k
        body_form.value = v

        form.testcase_body.append_entry(body_form)

    if not testcase_body:
        form.testcase_body.append_entry()

    testcase_verification = str_to_dict(interface_testcase_obj.testcase_verification)
    for k, v in testcase_verification.items():
        verification_form = VerificationForm()
        verification_form.key = k
        verification_form.value = v[0]
        verification_form.save = v[1]

        form.testcase_verification.append_entry(verification_form)
    if not testcase_verification:
        form.testcase_verification.append_entry()

    return form
