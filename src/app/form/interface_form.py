from flask_wtf import Form
from wtforms import StringField, BooleanField, FieldList, SelectField, TextAreaField, FormField
from wtforms_alchemy.fields import QuerySelectField
from wtforms.validators import length, data_required
from module.System_setting import SystemSetting
from .util import Method, get_all_module


class HeaderForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')
    desc = StringField(u"描述")

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(HeaderForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


class BodyForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')
    desc = StringField(u"描述")

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(BodyForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


class QueryForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')
    desc = StringField(u"描述")

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(QueryForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


def get_runner_setting():
    return SystemSetting.get_runner_setting()


class InterfaceFrom(Form):
    interface_body_type = ""
    interface_name = StringField(u'接口名称', [length(min=0, max=200),data_required(message= u'接口名不能为空')])
    interface_url = StringField(u'接口url', [length(min=0), data_required(message= u'接口url不能为空')])
    interface_method = SelectField(u"接口方法", choices=Method)
    runner_setting = QuerySelectField(u"当前环境", query_factory=get_runner_setting)
    module = QuerySelectField(u"所属模块", query_factory=get_all_module)
    interface_header = FieldList(FormField(HeaderForm), min_entries=1)
    interface_query = FieldList(FormField(QueryForm), min_entries=1)
    interface_data = FieldList(FormField(BodyForm), min_entries=1)
    interface_json = StringField()
    interface_desc = TextAreaField(u"接口描述")
    is_active = BooleanField('is_active')


def populate_interface(interface_obj):
    form = InterfaceFrom()
    form.interface_name.data = interface_obj.interface_name
    form.interface_url.data = interface_obj.interface_url
    form.interface_method.data = interface_obj.interface_method
    form.module.data = interface_obj.module
    form.interface_desc.data = interface_obj.interface_desc

    while len(form.interface_header) > 0:
        form.interface_header.pop_entry()

    while len(form.interface_query) > 0:
        form.interface_query.pop_entry()

    while len(form.interface_data) > 0:
        form.interface_data.pop_entry()

    headers = interface_obj.interface_header

    for header in headers:
        header_form = HeaderForm()
        header_form.key = header.get("name")
        header_form.value = header.get("value")
        header_form.desc = header.get("description")

        if header.get("name") == "Content-type":
            form.interface_body_type = header.get("value")

        form.interface_header.append_entry(header_form)

    if not headers:
        form.interface_header.append_entry()

    query = interface_obj.interface_query
    for q in query:
        query_form = QueryForm()
        query_form.key = q.get("name")
        query_form.value = q.get("value")
        query_form.desc = q.get("description")

        form.interface_query.append_entry(query_form)

    if not query:
        form.interface_query.append_entry()

    body = interface_obj.interface_body

    if form.interface_body_type == "application/json":
        form.interface_json.data = body

        form.interface_data.append_entry()
    else:
        for b in body:
            body_form = BodyForm()
            body_form.key = b.get("name")
            body_form.value = b.get("value")
            body_form.desc = b.get("description")

            form.interface_data.append_entry(body_form)

        form.interface_json.data = {}
        if not body:
            form.interface_data.append_entry()

    return form
