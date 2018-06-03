# -*- coding: utf-8 -*-
import six
import json
import yaml
from collections import OrderedDict
from swagger_py_codegen.parser import Swagger
from swagger_py_codegen.jsonschema import schema_var_name

from module.Module import Module
from module.Interface import Interface
from app import db


def get_data(file):
    if file.filename.endswith(".json"):
        data = json.loads(file.read())
    else:
        data = yaml.safe_load(file.read())
    return data




def get_module(module_name):
    module = Module.get_by_name(module_name)
    if len(module) == 0:
        module = Module()
        module.project_id = 1
        module.module_name = module_name
        module.module_version = u"未分配"
        module.module_developer = u"未分配"
        module.module_testers = u"未分配"
        module.module_desc = u"swagger自动插入"
        db.session.add(module)
        db.commit()
    else:
        module = module[0]
    return module


def init_parameters(parameters):

    headers = []
    body = []
    query = []
    for parameter in parameters:
        parameter_in = parameter["in"]
        if parameter_in == "headers":
            headers.append(parameter)
        if parameter_in == "query":
            query.append(parameter)
        if parameter_in in ("formData", "body"):
            body.append(parameter)

    return {"headers":headers, "body":body, "query":query}


def insert_data(file):
    data = get_data(file)

    try:
        data = build_data(data)
        tags = data.get("tags")
        for key, value in tags.items():
            interface_obj = Interface()
            interface_obj.interface_url = key[0]
            interface_obj.interface_method = key[1]
            interface_obj.module(get_module(value[0]))




    except Exception as e:
        raise e


a = {'tags': OrderedDict([(('/pay_content', 'GET'), ['payment'])]),
     'validators': OrderedDict([(('/pay_content', 'GET'), [{'name': 'merchant_id',
                                                            'description': '商户的ID(Mobi系统)',
                                                            'required': True,
                                                            'in': 'query',
                                                            'type': 'string'},
                                                           {'name': 'currency_code',
                                                            'description': '货币号 (BTC, ETH, LTC, BCC)',
                                                            'required': True,
                                                            'in': 'query',
                                                            'type': 'string'},
                                                           {'name': 'sign',
                                                            'description': '参数签名',
                                                            'required': True,
                                                            'in': 'query',
                                                            'type': 'string'}])]),
     'operationId': OrderedDict([(('/pay_content', 'GET'), 'pay_content')]),

     'scopes': OrderedDict([(('/pay_content', 'GET'), 'token')]),
     'filters': OrderedDict([(('/pay_content', 'GET'), {200: {'schema': "", 'headers': None}})])}
