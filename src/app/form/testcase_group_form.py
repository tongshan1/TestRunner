from wtforms_alchemy import ModelForm, ModelFieldList, QuerySelectField

from module.Testcasegroup import Testcasegroup, TestCaseType
from module.Module import Module


def get_modules():
    return Module.query


def get_types():
    return TestCaseType.query


class TestCaseGroupForm(ModelForm):
    class Meta:
        model = Testcasegroup
        exclude = ['datachange_createtime', 'datachange_lasttime', 'module_id', 'testcase_type']
        # include = ['testcase_group_name', 'testcase_desc', 'is_active']
        field_args = {
            'testcase_group_name': {'label: u"用例集名称'},
            'testcase_desc': {'label: u"用例集描述'},
            'is_active': {'label: u"是否可用'}
        }

    module = QuerySelectField(u'所属模块',
                              query_factory=get_modules,
                              get_label='module_name', allow_blank=False)
    type = QuerySelectField(u'用例集类型',
                              query_factory=get_types,
                              get_label='testcase_type', allow_blank=False)

