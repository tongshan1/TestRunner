
from flask_wtf import Form
from wtforms import StringField, BooleanField, FieldList, FormField, SelectField
from wtforms_alchemy.fields import QuerySelectField
from wtforms.validators import length, data_required
from module.System_setting import SystemSetting
from .util import Method, Type, get_all_module, str_to_dict


class HeaderForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(HeaderForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


class BodyForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(BodyForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


class QueryForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(QueryForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


class VerificationForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')
    save = BooleanField(u"保存")
    v_type = SelectField(u"类型", coerce=str, choices=Type)

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(VerificationForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


def get_runner_setting():
    return SystemSetting.get_runner_setting()


class TestInterfaceCaseFrom(Form):
    testcase_body_type = ""
    interface_url = StringField(u'接口url', [length(min=0), data_required(message=u'接口url不能为空')])
    testcase_name = StringField(u'接口名称', [data_required(message=u'接口名不能为空')])
    module = QuerySelectField(u"所属模块", query_factory=get_all_module)
    runner_setting = QuerySelectField(u"当前环境", query_factory=get_runner_setting)
    testcase_method = SelectField(u"接口方法", choices=Method)
    testcase_header = FieldList(FormField(HeaderForm), min_entries=1)
    testcase_query = FieldList(FormField(QueryForm), min_entries=1)
    testcase_data = FieldList(FormField(BodyForm), min_entries=1)
    testcase_json = StringField()
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

    while len(form.testcase_data) > 0:
        form.testcase_data.pop_entry()

    while len(form.testcase_verification) > 0:
        form.testcase_verification.pop_entry()

    testcase_header = interface_testcase_obj.testcase_header

    for k, v in testcase_header.items():
        header_form = HeaderForm()
        header_form.key = k
        header_form.value = v

        if k == "Content-type":
            form.testcase_body_type = v

        form.testcase_header.append_entry(header_form)

    if not testcase_header:
        form.testcase_header.append_entry()

    testcase_query = interface_testcase_obj.testcase_query
    for k, v in testcase_query.items():
        query_form = QueryForm()
        query_form.key = k
        query_form.value = v

        form.testcase_query.append_entry(query_form)

    if not testcase_query:
        form.testcase_query.append_entry()

    testcase_body = interface_testcase_obj.testcase_body

    if form.testcase_body_type == "application/json":
        form.testcase_json.data = testcase_body
        form.testcase_data.append_entry()
    else:
        for k, v in testcase_body.items():
            body_form = BodyForm()
            body_form.key = k
            body_form.value = v

            form.testcase_data.append_entry(body_form)
        form.testcase_json.data = {}
        if not testcase_body:
            form.testcase_data.append_entry()

    testcase_verification = interface_testcase_obj.testcase_verification
    for k, v in testcase_verification.items():
        verification_form = VerificationForm()
        verification_form.key = k
        verification_form.value = v[0]
        verification_form.save = v[1]
        verification_form.v_type = v[2]

        form.testcase_verification.append_entry(verification_form)
    if not testcase_verification:
        form.testcase_verification.append_entry()

    return form


def populate_interface(interface_obj):
    form = TestInterfaceCaseFrom()
    form.interface_url.data = interface_obj.interface_url
    form.module.data = interface_obj.module
    form.testcase_method.data = interface_obj.interface_method

    while len(form.testcase_header) > 0:
        form.testcase_header.pop_entry()

    while len(form.testcase_query) > 0:
        form.testcase_query.pop_entry()

    while len(form.testcase_data) > 0:
        form.testcase_data.pop_entry()

    testcase_header = interface_obj.interface_header

    for header in testcase_header:
        header_form = HeaderForm()
        header_form.key = header.get("name")
        header_form.value = header.get("value")

        if header.get("name") == "Content-type":
            form.testcase_body_type = header.get("value")

        form.testcase_header.append_entry(header_form)

    if not testcase_header:
        form.testcase_header.append_entry()

    testcase_query = interface_obj.interface_query
    for query in testcase_query:
        query_form = QueryForm()
        query_form.key = query.get("name")
        query_form.value = query.get("value")

        form.testcase_query.append_entry(query_form)

    if not testcase_query:
        form.testcase_query.append_entry()

    testcase_body = interface_obj.interface_body

    if form.testcase_body_type == "application/json":
        json_data = {}
        for body in testcase_body:
            json_data[body.get("name")] = body.get("value")
        form.testcase_json.data = json_data
        form.testcase_data.append_entry()
    else:
        for body in testcase_body:
            body_form = BodyForm()
            body_form.key = body.get("name")
            body_form.value = body.get("value")

            form.testcase_data.append_entry(body_form)
        form.testcase_json.data = {}

        if not testcase_body:
            form.testcase_data.append_entry()

    return form
