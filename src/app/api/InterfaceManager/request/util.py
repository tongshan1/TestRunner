import re


def get_variable(str):
    """
    获取{$ key $}这样形式的key值
    :return:
    """
    key_re = "(\{\$.*?\$\})"
    