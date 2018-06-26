from flask_wtf import Form
from wtforms.fields import BooleanField, IntegerField
from wtforms.validators import data_required


class TestCaseTestGroupForm(Form):
    testcase_group_id = IntegerField(u"用例集名称", [data_required(message= u'用例集名称不能为空')])
    testcase_id = IntegerField(u'用例名称', [data_required(message= u'用例名称不能为空')])
    is_active = BooleanField(u'是否可用')
