# -*- coding: utf-8 -*-
import six
import json
import yaml
from collections import OrderedDict
from swagger_py_codegen.parser import Swagger
from swagger_py_codegen.jsonschema import schema_var_name


def get_data(file):
    if file.filename.endswith(".json"):
        data = json.loads(file.read())
    else:
        data = yaml.safe_load(file.read())
    return data


def build_data(data):
    swagger = Swagger(data)

    validators = OrderedDict()  # (endpoint, method) = {'body': schema_name or schema, 'query': schema_name, ..}
    filters = OrderedDict()  # (endpoint, method) = {'200': {'schema':, 'headers':, 'examples':}, 'default': ..}
    scopes = OrderedDict()  # (endpoint, method) = [scope_a, scope_b]
    operationId = OrderedDict()
    tags = OrderedDict()

    schemas = OrderedDict([(schema_var_name(path), swagger.get(path)) for path in swagger.definitions])

    # path parameters
    for path, _ in swagger.search(['paths', '*']):

        # methods
        for p, data in swagger.search(path + ('*',)):
            if p[-1] not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                continue

            endpoint = p[1]  # p: ('paths', '/some/path', 'method')
            method = p[-1].upper()

            # parameters as schema
            parameters = data.get('parameters')
            params = []
            # 这边有点小问题，array怎么搞？
            if parameters:
                for param in parameters:
                    if param.get("name") == "body" and "schema" in param.keys():

                        values = list(param["schema"]["properties"].values())

                        for value in values:
                            value["in"] = "body"
                        params += values

                        del schemas[str(param["schema"])]
                    else:
                        params.append(param)

            validators[(endpoint, method)] = params

            # responses
            responses = data.get('responses')
            if responses:
                filter = {}
                for status, res_data in six.iteritems(responses):
                    if isinstance(status, int) or status.isdigit():
                        filter[int(status)] = dict(
                            headers=res_data.get('headers'),
                            schema=res_data.get('schema')
                        )
                filters[(endpoint, method)] = filter

            # operationId
            operationId[(endpoint, method)] = data.get('operationId')

            # tags
            tags[(endpoint, method)] = data.get('tags')


            # scopes
            securitys = data.get('security') or []
            if len(securitys) == 0:
                scopes[(endpoint, method)] = []
            else:
                for security in securitys:
                    scopes[(endpoint, method)] = list(security.keys()).pop()
                    break
    data = dict(
        schemas=schemas,
        validators=validators,
        filters=filters,
        scopes=scopes,
        operationId=operationId,
        tags=tags
        # merge_default=getsource(merge_default),
        # normalize=getsource(normalize)
    )

    return data


def insert_data(file):
    data = get_data(file)

    try:
        data = build_data(data)
        tags = data.get("tags")
        for key, value in tags.items():
            pass
    except Exception as e:
        raise e


a = {'tags': OrderedDict([(('/pay_content', 'GET'), ['payment'])]),
     'validators': OrderedDict([(('/pay_content', 'GET'), [{'name': 'merchant_id',
                                                            'description': '商户的ID(Mobi系统)',
                                                            'required': True,
                                                            'in': 'query',
                                                            'type': 'string'}, {
                                                               'name': 'currency_code',
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
