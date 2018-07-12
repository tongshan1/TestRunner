# -*- coding: utf-8 -*-

from wtforms_alchemy import ModelForm, QuerySelectField

from app.module.Module import Module
from app.module.Project import Project


def get_projects():
    return Project.query


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        exclude = ['datachange_createtime', 'datachange_lasttime', 'project_id']
        field_args = {
            'module_name': {'label': u'模块名'},
            'module_testers': {'label': u'测试人员'},
            'module_developer': {'label': u'开发人员'},
            'module_version': {'label': u'模块版本'},
            'module_desc': {'label': '模块描述'},
            'is_active': {'label': '是否可用'}
        }

    project = QuerySelectField(u'项目名称',
                               query_factory=get_projects,
                               get_label='project_name', allow_blank=False)
