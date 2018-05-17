from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField,IntegerField
from wtforms.validators import length, data_required


class TestCaseFrom(Form):
    interface_url = StringField('interface_url', [length(min=0, max=100), data_required(message= u'接口url不能为空')])
    testcase_name = StringField('testcase_name', [ data_required(message= u'接口名不能为空')])
    module_id = IntegerField("module_id", data_required(message= u'所属某块不能为空'))
    testcase_method = StringField('testcase_method', [length(min=0, max=100), data_required(message= u'testcase_method不能为空')])
    testcase_header = StringField('testcase_header')
    testcase_body = StringField('testcase_body')
    testcase_verification = StringField('testcase_body')
    is_active = BooleanField('is_active')

