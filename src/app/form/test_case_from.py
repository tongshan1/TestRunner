from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField,IntegerField
from wtforms.validators import length, data_required


class TestCaseFrom(Form):
    interface_url = StringField('interface_url', [length(min=0, max=100), data_required(message= u'接口url不能为空')])
    testcase_name = StringField('testcase_name', [ data_required(message= u'接口名不能为空')])
    testcase_method = StringField('testcase_method', [length(min=0, max=100), data_required(message= u'testcase_method不能为空')])
    testcase_header = StringField('testcase_header', [data_required(message= u'interface_header不能为空')])
    testcase_body = StringField('testcase_body')
    testcase_method = StringField('testcase_method', [length(min=0, max=100), data_required(message= u'interface_method不能为空')])
    is_active = BooleanField('is_active')

