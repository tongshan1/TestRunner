import json
from . import app_filter
from app.logger import logger


@app_filter.app_template_filter("str_json")
def str_json(data):
    """

    :param str: [{name:key1, value:value, require:True, description: desc}]
    :return:
    """
    try:
        data = json.loads(data)
        return data
    except Exception:
        logger.error("data 转化失败")
    return []


@app_filter.app_template_filter("set_body")
def set_body(data, interface_headers):
    """
    设置body
    :param data:
    :return:
    """