# -*- coding: utf-8 -*-
import six
import json
import yaml
from collections import OrderedDict

from module.Module import Module
from module.Interface import Interface
from .schema_generator import build_data
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
        db.session.commit()
    else:
        module = module[0]
    return module


def init_parameters(parameters):
    headers = []
    body = []
    query = []
    for parameter in parameters:
        parameter_in = parameter.pop("in")
        parameter.pop("type")
        parameter.pop("required")
        parameter["value"] = ""
        if parameter_in == "headers":
            headers.append(parameter)
        if parameter_in == "query":
            query.append(parameter)
        if parameter_in in ("formData", "body"):
            body.append(parameter)

    return {"headers": json.dumps(headers, ensure_ascii=False), "body": json.dumps(body, ensure_ascii=False), "query": json.dumps(query, ensure_ascii=False)}


def insert_data(file):
    data = get_data(file)

    try:
        data = build_data(data)

        """
        data = {'tags': OrderedDict([(('/endpoint', 'method'), 'tag')]),
                    'validators': OrderedDict([(('/endpoint', 'method'), [{'name': 'param_name',
                                                            'description': 'param_desc',
                                                            'required': True,
                                                            'in': 'query',
                                                            'type': 'string'},
                                                           {'name': 'param_name',
                                                            'description': 'param_desc',
                                                            'required': True,
                                                            'in': 'query',
                                                            'type': 'string'},
                                                           {'name': 'param_name',
                                                            'description': 'param_desc',
                                                            'required': True,
                                                            'in': 'query',
                                                            'type': 'string'}])]),
                    'operationId': OrderedDict([(('/endpoint', 'method'), 'operationId')]),

                    'scopes': OrderedDict([(('/endpoint', 'method'), 'token')]),
                    'filters': OrderedDict([(('/endpoint', 'method'), {200: {'schema': "", 'headers': None}})])}
        """

        # tags = [(endpoint, method): [tags]]
        tags = data.get("tags")
        param = data.get("validators")
        operationId = data.get("operationId")
        desc = data.get("desc")
        for key, value in tags.items():
            interface_obj = Interface()
            interface_obj.interface_name = operationId[key]
            interface_obj.interface_url = key[0]
            interface_obj.interface_method = key[1]
            interface_obj.module = get_module(value)
            params = init_parameters(param[key])
            interface_obj.interface_header=params["headers"]
            interface_obj.interface_query=params["query"]
            interface_obj.interface_bod=params["body"]
            interface_obj.interface_desc=desc[key]
            db.session.add(interface_obj)

        db.session.commit()

    except Exception as e:
        raise e
