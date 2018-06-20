from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField, FieldList, FormField
from wtforms.validators import length, data_required


class ValueForm(Form):
    key = StringField(u'变量名')
    value = StringField(u'变量值')

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(ValueForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


class SettingFrom(Form):
    key = StringField(u"运行环境名称", [length(min=0), data_required(message=u'setting_name不能为空')])
    desc = StringField(u"简述")
    value = FieldList(FormField(ValueForm), label=u"变量列表", min_entries=1)


def populate_setting(setting_obj):

    setting_form = SettingFrom()
    setting_form.key.data = setting_obj.key
    setting_form.desc.data = setting_obj.desc

    while len(setting_form.value)>0:
        setting_form.value.pop_entry()

    value = setting_obj.value
    for k, v in value.items():
        value_form = ValueForm()
        value_form.key = k
        value_form.value = v

        setting_form.value.append_entry(value_form)

    return setting_form
