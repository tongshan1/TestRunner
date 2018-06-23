import re
import json
import ast
from module.System_setting import SystemSetting
from app.logger import logger


class Variable(dict):
    def __init__(self):
        super().__init__()


variable = Variable()


def replace_variable(runner_setting, tmp):
    """
    获取{$ key $}这样形式的key值
    请求中设置的变量优先与环境变量
    :return:
    """
    if type(tmp) != str:
        tmp = str(tmp)

    regex = re.compile("\{\$(.+?)\$\}")
    keys = regex.findall(tmp)

    runner_setting = SystemSetting.get_by_id(runner_setting)
    variable_in_setting = runner_setting.value

    for key in keys:
        value = variable.get(key, "")
        value_in_setting = variable_in_setting.get(key, "")
        tmp = tmp.replace("{$"+key+"$}", value_in_setting).replace("{$"+key+"$}", value)
    return tmp


def set_variable(key, value):
    """
    提取 保存变量
    :param str:
    :return:
    """
    variable[key] = value


def str_to_dict(tmp):
    try:
        if type(tmp) == str:
            return ast.literal_eval(tmp)
        else:
            return tmp
    except ValueError:
        return tmp