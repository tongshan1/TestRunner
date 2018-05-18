from flask_wtf import Form
from wtforms_alchemy.fields import StringField, QuerySelectField
from wtforms.fields import BooleanField, IntegerField, HiddenField
from wtforms.validators import length, data_required


class TestCaseTestGroupForm(Form):
    testcase_group_id = IntegerField(u"用例集名称", [data_required(message= u'用例集名称不能为空')])
    testcase_id = IntegerField(u'用例名称', [data_required(message= u'用例名称不能为空')])
    # testcase_execution_order = IntegerField(u'用例执行顺序', [length(min=0, max=100), data_required(message= u'用例执行顺序不能为空')])
    is_active = BooleanField(u'是否可用')
