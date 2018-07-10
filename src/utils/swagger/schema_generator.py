from collections import OrderedDict
from swagger_py_codegen.base import CodeGenerator
from swagger_py_codegen.parser import Swagger
from swagger_py_codegen.jsonschema import schema_var_name, Schema
import six


def build_data(data):
    swagger = Swagger(data)

    validators = OrderedDict()  # (endpoint, method) = {'body': schema_name or schema, 'query': schema_name, ..}
    filters = OrderedDict()  # (endpoint, method) = {'200': {'schema':, 'headers':, 'examples':}, 'default': ..}
    scopes = OrderedDict()  # (endpoint, method) = [scope_a, scope_b]
    operationId = OrderedDict()
    tags = OrderedDict()
    desc= OrderedDict()

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
            name = data.get('operationId')
            if name in ["", None]:
                name = "{}_{}".format(method, endpoint.replace("/", "_"))
            operationId[(endpoint, method)] = name

            # tags
            tag = data.get('tags')
            if len(tag) < 1:
                tag = u"未分配"
            else:
                tag = tag[0]
            tags[(endpoint, method)] = tag

            # summary and description
            desc[(endpoint, method)] = "{0} {1}".format(data.get("summary"), data.get("description"))

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
        tags=tags,
        desc=desc
        # merge_default=getsource(merge_default),
        # normalize=getsource(normalize)
    )

    return data


class SchemaGenerator(CodeGenerator):

    def _process(self):
        yield Schema(build_data(self.swagger))