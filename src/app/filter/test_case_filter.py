from . import app_filter
from app.logger import logger


@app_filter.app_template_filter("set_test_case_data")
def set_test_case_data(testcase_data, type):
    """
    设置body
    :param data:
    :return:
    """
    # data = testcase_data
    # if type != "application/json":
    #     data.pop_entry()
    #     data.append_entry()

    return testcase_data


@app_filter.app_template_filter("set_test_case_json_data")
def set_test_case_json_data(data, type):
    """
    设置body
    :param data:
    :return:
    """
    json_data = {}

    if type == "application/json":
        for d in data:
            json_data[d.key.data] = d.value.data

    return json_data
