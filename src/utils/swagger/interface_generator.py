import six
import re
from swagger_py_codegen.parser import Swagger
from swagger_py_codegen.base import CodeGenerator
from swagger_py_codegen.jsonschema import Schema, build_default, SchemaGenerator
from collections import OrderedDict

SUPPORT_METHODS = ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']


def _location(swagger_location):
    location_map = {
        'body': 'json',
        'header': 'headers',
        'formData': 'form',
        'query': 'args'
    }
    return location_map.get(swagger_location)


def _swagger_to_url(url, swagger_path_node):
    types = {
        'integer': 'int',
        'long': 'int',
        'float': 'float',
        'double': 'float'
    }
    node = swagger_path_node
    params = re.findall(r'\{([^\}]+?)\}', url)
    url = re.sub(r'{(.*?)}', '<\\1>', url)

    def _type(parameters):
        for p in parameters:
            if p.get('in') != 'path':
                continue
            t = p.get('type', 'string')
            if t in types:
                yield '<%s>' % p['name'], '<%s:%s>' % (types[t], p['name'])

    for old, new in _type(node.get('parameters', [])):
        url = url.replace(old, new)

    for k in SUPPORT_METHODS:
        if k in node:
            for old, new in _type(node[k].get('parameters', [])):
                url = url.replace(old, new)

    return url, params


if six.PY3:
    def _remove_characters(text, deletechars):
        return text.translate({ord(x): None for x in deletechars})
else:
    def _remove_characters(text, deletechars):
        return text.translate(None, deletechars)


def _path_to_endpoint(swagger_path):
    return _remove_characters(
        swagger_path.strip('/').replace('/', '_').replace('-', '_'),
        '{}')


def _path_to_resource_name(swagger_path):
    return _remove_characters(swagger_path.title(), '{}/_-')


class InterfaceGenerator(CodeGenerator):
    dependencies = [SchemaGenerator]

    def __init__(self, swagger):
        super(InterfaceGenerator, self).__init__(swagger)
        self.with_spec = False

    def _dependence_callback(self, code):
        if not isinstance(code, Schema):
            return code
        schemas = code
        # schemas default key likes `('/some/path/{param}', 'method')`
        # use flask endpoint to replace default validator's key,
        # example: `('some_path_param', 'method')`
        validators = OrderedDict()
        for k, v in six.iteritems(schemas.data['validators']):
            validators[(_path_to_endpoint(k[0]), k[1])] = v

        # filters
        filters = OrderedDict()
        for k, v in six.iteritems(schemas.data['filters']):

            filters[(_path_to_endpoint(k[0]), k[1])] = v

        # scopes
        scopes = OrderedDict()
        for k, v in six.iteritems(schemas.data['scopes']):
            scopes[(_path_to_endpoint(k[0]), k[1])] = v

        schemas_1 = OrderedDict()
        print(self.swagger)
        # for k, v in six.iteritems(schemas.data['merge_default']):
        #     print(k)
        #     print(v)

        schemas.data['validators'] = validators
        schemas.data['filters'] = filters
        schemas.data['scopes'] = scopes
        self.schemas = schemas
        self.validators = validators
        self.filters = filters

        return schemas

    def _process_data(self):
        views = []  # [{'endpoint':, 'name':, url: '', params: [], methods: {'get': {'requests': [], 'response'}}}, ..]
        for paths, data in self.swagger.search(['paths', '*']):
            swagger_path = paths[-1]
            url, params = _swagger_to_url(swagger_path, data)
            endpoint = _path_to_endpoint(swagger_path)
            name = _path_to_resource_name(swagger_path)

            methods = OrderedDict()
            for method in SUPPORT_METHODS:
                if method not in data:
                    continue
                methods[method] = {}
                validator = self.validators.get((endpoint, method.upper()))
                if validator:
                    methods[method]['requests'] = list(validator.keys())

                for status, res_data in six.iteritems(data[method].get('responses', {})):
                    if isinstance(status, int) or status.isdigit():
                        example = res_data.get('examples', {}).get('application/json')

                        if not example:
                            example = build_default(res_data.get('schema'))
                        response = example, int(status), build_default(res_data.get('headers'))
                        methods[method]['response'] = response
                        break

            views.append(dict(
                url=url,
                params=params,
                endpoint=endpoint,
                methods=methods,
                name=name
            ))

        return views

    def _get_oauth_scopes(self):
        for path, scopes in self.swagger.search(('securityDefinitions', '*', 'scopes')):
            return scopes
        return None

    def _process(self):
        views = self._process_data()
        for view in views:
            print(view)

    def generate(self):
        for clz in self.dependencies:
            dependence = clz(self.swagger)
            g = dependence.generate()
            for code in g:
                a = self._dependence_callback(code).data["validators"]


if __name__ == "__main__":
    import yaml

    tmp = "/Users/sara/Desktop/payment.yaml"

    with open(tmp, encoding='utf8') as f:
        data = yaml.load(f)

    swagger = Swagger(data)
    interface = InterfaceGenerator(swagger)
    interface.generate()