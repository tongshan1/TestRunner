from marshmallow import Schema, fields


class InterfaceSchema(Schema):
    id = fields.String()
    module_id = fields.Integer()
    interface_name = fields.String()
    interface_url = fields.String()
    interface_header = fields.Dict()
    interface_query = fields.Dict()
    interface_body = fields.Dict()
    interface_method = fields.String()
    is_active = fields.Boolean()
    datachange_createtime = fields.Date()
    datachange_lasttime = fields.Date()
