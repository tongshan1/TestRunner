import json
from . import app_filter
from app.logger import logger


@app_filter.app_template_filter("set_header")
def str_json(headers):
    """

    :param header: [{name:key1, value:value, require:True, description: desc}]
    :return:
    """
    headers = json.loads(headers)
    logger.debug(headers)
    return headers


