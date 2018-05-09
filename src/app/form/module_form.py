from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField,IntegerField
from wtforms.validators import length, data_required


class ModuleFrom(Form):
    project_id = IntegerField('project_id', [ data_required(message= u'项目名不能为空')])
    module_name = StringField('module_name', [length(min=4, max=50), data_required(message= u'模块名不能为空')])
    module_testers = StringField('module_testers', [length(min=4, max=50), data_required(message= u'测试人员不能为空')])
    module_developer = StringField('module_developer', [length(min=4, max=50), data_required(message= u'开发人员不能为空')])
    module_version = StringField('module_version', [length(min=4, max=100), data_required(message= u'模块版本不能为空')])
    module_desc = StringField('module_desc', [length(min=4, max=500), data_required(message= u'模块描述不能为空')])
    is_active = BooleanField('is_active')
    submit = SubmitField("submit")
