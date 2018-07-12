# -*- coding: utf-8 -*-

from wtforms_alchemy import ModelForm

from app.module.Project import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['datachange_createtime', 'datachange_lasttime']
        field_args = {
            'project_name': {'label': u'项目名称'},
            'project_testers': {'label': u'测试人员'},
            'project_developer': {'label': u'开发人员'},
            'project_version': {'label': u'项目版本'},
            'project_desc': {'label': u'项目简介'},
            'is_active': {'label': '是否可用'}
        }
