from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import length, data_required


class TestCaseGroupForm(Form):
    testcase_group_name = StringField('testcase_group_name', [length(min=4, max=50), data_required(message= u'项目名不能为空')])
    module_id = IntegerField('module_id', [ data_required(message= u'测试人员不能为空')])
    testcase_type = IntegerField('testcase_type', [ data_required(message= u'开发人员不能为空')])
    testcase_desc = StringField('testcase_desc', [length(min=4, max=100), data_required(message= u'项目版本不能为空')])
    is_active = BooleanField('is_active')
    submit = SubmitField("submit")