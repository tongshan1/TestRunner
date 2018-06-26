from wtforms import TextAreaField
from wtforms_alchemy import ModelForm
from wtforms_alchemy.fields import StringField, QuerySelectField
from wtforms.validators import length, data_required

from .util import get_runner_setting, get_types, get_all_module


class TestCaseGroupForm(ModelForm):
    testcase_group_name = StringField(u'用例集名', [length(min=0, max=100), data_required(message= u'用例集名不能为空')])
    testcase_desc = TextAreaField(u"接口描述")
    module = QuerySelectField(label=u'所属模块',query_factory=get_all_module)
    type = QuerySelectField(label=u'用例集类型',query_factory=get_types)
    runner_setting = QuerySelectField(label=u"运行环境", query_factory=get_runner_setting)