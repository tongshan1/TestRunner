import re
import json
from module.System_setting import SystemSetting
from app.logger import logger


class Variable(dict):
    def __init__(self):
        super().__init__()


variable = Variable()
variable["ts"] = "1527055281"
variable["hash"] = "15215b8b123c9e7ed2bc858eb398606bdcfe76133f7d98fa832022523298dbc0s"


def replace_variable(runner_setting, str):
    """
    获取{$ key $}这样形式的key值
    请求中设置的变量优先与环境变量
    :return:
    """

    regex = re.compile("\{\$(.+?)\$\}")
    keys = regex.findall(str)

    runner_setting = SystemSetting.get_by_id(runner_setting)
    variable_in_setting = runner_setting.value

    for key in keys:
        value = variable.get(key, "")
        value_in_setting = variable_in_setting.get(key, "")
        str = str.replace("{$"+key+"$}", value_in_setting).replace("{$"+key+"$}", value)
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