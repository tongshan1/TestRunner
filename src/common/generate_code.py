# -*- coding: utf-8 -*-
import six
import os
import requests
import json
import yaml
from swagger_py_codegen.parser import Swagger
from swagger_py_codegen.jsonschema import schema_var_name
from collections import OrderedDict


def download_doc(url):
    """
    获取最新的api文档
    :return:
    """
    response = requests.get(url)
    if url.endswith(".json"):
        data = json.loads(response.text)
    else:
        data = yaml.safe_load(response.text)
    return data


def build_data(data):
    swagger = Swagger(data)

    validators = OrderedDict()  # (endpoint, method) = {'body': schema_name or schema, 'query': schema_name, ..}
    filters = OrderedDict()  # (endpoint, method) = {'200': {'schema':, 'headers':, 'examples':}, 'default': ..}
    scopes = OrderedDict()  # (endpoint, method) = [scope_a, scope_b]
    operationId= OrderedDict()
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

    return validators, filters, scopes, schemas, operationId, tags


def generate_code():

    # if os.path.exists(api_file_path) is False:
    #     os.makedirs(api_file_path)

    data = download_doc("https://staging-mobi.mobiapp.cn:8443/static/files/API_V_2_0.yaml")

    validators, filters, scopes, schemas, operationId, tags = build_data(data)

    tag_data = []
    for k, v in scopes.items():
        api_data = {}
        response = filters[k][200]["schema"]
        params = validators.get(k) or {}
        ID = operationId.get(k)
        api_data["params"] = params
        api_data["response"] = response
        api_data["security"] = v or {}
        api_data["operationId"] = ID
        tag = tags[k][0]
        if tag not in tag_data:
           tag_data.append(tag)

    return tag_data

    # env = Environment(loader=FileSystemLoader(TMP_DOC_PATH), trim_blocks=True)
    #
    # definitions_file = os.path.join(api_file_path, "definitions")
    # template = env.get_template(TMP_DEFINITIONS_NAME.format(project))
    #
    # with open(definitions_file+".py", "w", encoding="utf-8") as f:
    #     f.write(template.render(definitions=schemas))
    #
    # for tag, data in tag_data.items():
    #     api_file = os.path.join(api_file_path, tag)
    #
    #     template = env.get_template(TMP_DOC_NAME.format(project))
    #     with open(api_file+".py", "w", encoding="utf-8") as f:
    #
    #         f.write(template.render(request='request', tpl_data=data), )

# if __name__ == "__main__":
#     yml = "/Users/sara/PycharmProjects/auto_api_test/config/api_doc/mobi/mall.yaml"
#     api = "/Users/sara/PycharmProjects/auto_api_test/src/api/mobi/mall"
#
#     generate_code(yml, api)
