import json
from . import app_filter
from app.logger import logger


@app_filter.app_template_filter("set_test_case_form_data")
def set_form_data(data, headers):
    """
    设置body
    :param data:
    :return:
    """
    try:

        for header in headers:
            if header["name"] == "Content-type" and header["value"] == "application/x-www-form-urlencoded":
                return data
    except Exception:
        logger.error("data 转化失败")
    return []


@app_filter.app_template_filter("set_test_case_urlencoded_data")
def set_urlencoded_data(data, headers):
    """
    设置body
    :param data:
    :return:
    """
    try:
        is_set_body_type = False

        for header in headers:
            if header["name"] == "Content-type":
                is_set_body_type = True
                if header["value"] == "application/x-www-form-urlencoded":
                    return data

        if not is_set_body_type:
            return data

    except Exception as e:
        logger.error(e)
        logger.error("data 转化失败")
    return []


@app_filter.app_template_filter("set_test_case_form_data")
def set_form_data(data, headers):
    """
    设置body
    :param data:
    :return:
    """
    try:

        for header in headers:
            if header["name"] == "Content-type":
                if header["value"] == "application/form-data":
                    return data

    except Exception as e:
        logger.error(e)
        logger.error("data 转化失败")
    return []


@app_filter.app_template_filter("set_test_case_json_data")
def set_json_data(data, headers):
    """
    设置body
    :param data:
    :return:
    """
    json_data = {}
    try:

        for header in headers:
            if header["name"] == "Content-type":
                if header["value"] == "application/json":
                    json_data[data["name"]] = data["value"]
                    return json_data

    except Exception as e:
        logger.error(e)
        logger.error("data 转化失败")
    return json_data