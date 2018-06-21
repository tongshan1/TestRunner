from . import app_filter
from app.logger import logger


@app_filter.app_template_filter("set_test_case_form_data")
def set_test_case_form_data(data, type):
    """
    设置body
    :param data:
    :return:
    """

    if type != "application/form-data":
        data.pop_entry()
        data.append_entry()

    return data


@app_filter.app_template_filter("set_test_case_urlencoded_data")
def set_test_case_urlencoded_data(data, type):
    """
    设置body
    :param data:
    :return:
    """
    if type != "application/x-www-form-urlencoded" and type != "":
        data.pop_entry()
        data.append_entry()
    return data



@app_filter.app_template_filter("set_test_case_json_data")
def set_test_case_json_data(data, type):
    """
    设置body
    :param data:
    :return:
    """
    json_data = {}

    if type == "application/json":
        json_data[data.key.data] = data.value.data

    return json_data
