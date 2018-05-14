from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField,IntegerField
from wtforms.validators import length, data_required


class InterfaceFrom(Form):
    interface_name = StringField('interface_name', [ data_required(message= u'接口名不能为空')])
    interface_url = StringField('interface_url', [length(min=4, max=50), data_required(message= u'接口url不能为空')])
    interface_header = StringField('interface_header', [length(min=4, max=50), data_required(message= u'interface_header不能为空')])
    interface_body = StringField('interface_body')
    interface_method = StringField('interface_method', [length(min=4, max=100), data_required(message= u'interface_method不能为空')])
    is_active = BooleanField('is_active')