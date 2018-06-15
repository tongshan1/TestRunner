from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField, FieldList, FormField
from wtforms.validators import length, data_required


class VariableForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')


class RunnerSettingFrom(Form):
    setting_name = StringField(u"运行环境名称", [length(min=0), data_required(message=u'setting_name不能为空')])
    setting_desc = StringField(u"简述")
    setting_variables = FieldList(FormField(VariableForm), label=u"变量列表", min_entries=2)
