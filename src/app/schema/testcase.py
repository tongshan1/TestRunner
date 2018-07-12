from marshmallow import Schema, fields


class TestCaseSchema(Schema):
    id = fields.Integer()
    interface_url = fields.String()
    testcase_name = fields.String()
    module_id= fields.Integer()
    testcase_method = fields.String()
    testcase_header = fields.Dict()
    testcase_query = fields.Dict()
    testcase_body = fields.Dict()
    testcase_verification = fields.Dict()
    is_active = fields.Boolean()
    datachange_createtime = fields.Date()
    datachange_lasttime = fields.Date()

