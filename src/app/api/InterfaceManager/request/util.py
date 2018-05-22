import re
import json


class Variable(dict):
    def __init__(self):
        super().__init__()


variable = Variable()


def replace_variable(str):
    """
    获取{$ key $}这样形式的key值
    :return:
    """

    regex = re.compile("\{\$(.+?)\$\}")
    keys = regex.findall(str)

    for key in keys:
        value = variable.get(key)
        print(value)
        str = str.replace("{$"+key+"$}", value)

    return str


def set_variable(key, value):
    """
    提取 保存变量
    :param str:
    :return:
    """
    variable[key] = value


def str_to_dict(str):
    try:

        str
        json.loads(str)
    except ValueError:
        raise


str = '{"ret":true}'

print(str_to_dict(str))