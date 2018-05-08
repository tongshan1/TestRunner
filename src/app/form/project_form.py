from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import length, data_required


class ProjectFrom(Form):
    project_name = StringField('project_name', [length(min=4, max=50), data_required(message= u'项目名不能为空')])
    project_testers = StringField('project_testers', [length(min=4, max=50), data_required(message= u'测试人员不能为空')])
    project_developer = StringField('project_developer', [length(min=4, max=50), data_required(message= u'开发人员不能为空')])
    project_version = StringField('project_developer', [length(min=4, max=100), data_required(message= u'项目版本不能为空')])
    project_desc = StringField('project_desc', [length(min=4, max=500), data_required(message= u'项目描述不能为空')])
    is_active = BooleanField('is_active')
    submit = SubmitField("submit")
