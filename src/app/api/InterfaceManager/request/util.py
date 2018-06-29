import re
import ast
from module.System_setting import SystemSetting
import plugin
from app.logger import logger


class Variable(dict):
    def __init__(self):
        super().__init__()


variable = Variable()
variable["pin"] = "000000"


def replace_variable(runner_setting, tmp):
    """
    获取{$ key $}这样形式的key值
    请求中设置的变量优先与环境变量
    变量优于方法
    :return:
    """
    if type(tmp) != str:
        tmp = str(tmp)

    regex_param = re.compile("\{\$(.+?)\$\}")
    keys = regex_param.findall(tmp)

    runner_setting = SystemSetting.get_by_id(runner_setting)
    variable_in_setting = runner_setting.value
    for key in keys:
        value = None

        setting_value = variable_in_setting.get(key, None)

        if setting_value is not None:
            value = setting_value

        variable_value = variable.get(key, None)
        if variable_value is not None:
            value = variable_value

        if value is not None:
            tmp = tmp.replace("{$"+key+"$}", value)
        else:
            logger.error("没有设置该变量：{0}".format(key))

    logger.error(tmp)
    regex_func = re.compile("\(\$(.+?)\$\)")
    keys = regex_func.findall(tmp)
    logger.error(keys)

    for key in keys:
        func_value = replace_variable_plugin(key)
        if func_value is not None:
            tmp = tmp.replace("($"+key+"$)", func_value)
        else:
            logger.error("没有设置该变量：{0}".format(key))

    logger.error(tmp)
    return tmp


def replace_variable_plugin(func_value):
    """
    根据 方法 动态获得值
    :param func_name:
    :return:
    """

    try:
        name = func_value[:func_value.index("(")]
        regex = re.compile("\((.+?)\)")
        param = regex.findall(func_value)
        if hasattr(plugin, name):
            func = getattr(plugin, name)
            if param:
                param = param[0].split(",")
                return func(*param)
            else:
                return func()
        else:
            logger.error("找不到{0}".format(func_value))
            return ""
    except Exception as e:
        logger.error("{0}变量方法运行出错".format(func_value))
        logger.error(str(e))
        return ""


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