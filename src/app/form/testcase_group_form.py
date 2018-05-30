from wtforms_alchemy import ModelForm
from wtforms_alchemy.fields import StringField, QuerySelectField
from wtforms.fields import BooleanField
from wtforms.validators import length, data_required

from module.Testcasegroup import Testcasegroup, TestCaseType
from module.Module import Module


def get_modules():
    return Module.get_all()


def get_types():
    return TestCaseType.get_all()


class TestCaseGroupForm(ModelForm):
    testcase_group_name = StringField(u'用例集名', [length(min=0, max=100), data_required(message= u'用例集名不能为空')])
    testcase_desc = StringField(u'用例集描述', [length(min=0, max=100), data_required(message= u'用例集描述不能为空')])
    is_active = BooleanField(u'是否可用')
    module = QuerySelectField(label=u'所属模块',query_factory=get_modules)
    type = QuerySelectField(label=u'用例集类型',query_factory=get_types)

