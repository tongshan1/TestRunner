import re
import json


class Variable(dict):
    def __init__(self):
        super().__init__()


variable = Variable()
variable["ts"] = "1527055281"
variable["hash"] = "15215b8b123c9e7ed2bc858eb398606bdcfe76133f7d98fa832022523298dbc0s"


def replace_variable(str):
    """
    获取{$ key $}这样形式的key值
    :return:
    """

    regex = re.compile("\{\$(.+?)\$\}")
    keys = regex.findall(str)

    for key in keys:
        value = variable.get(key)
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

        return json.loads(str)
    except ValueError:
        return str