from . import app_filter
from module.Report import Report


@app_filter.app_template_filter("filter_result")
def filter_result(result):
    """

    :param key:
    :return:
    """
    if result:
        return u"成功"
    else:
        return u"失败"


@app_filter.app_template_filter("filter_testcase_result")
def filter_testcase_result(reuslt):
    """
    过滤测试结果
    result : 1 pass
                 2 error
                 3 fail
    :param reuslt:
    :return:
    """
    if reuslt == 1:
        return u"成功"

    if reuslt == 2:
        return u"错误"
    if reuslt == 3:
        return u"失败"


@app_filter.app_template_filter("filter_testcase_class")
def filter_testcase_class(result):
    """
    过滤测试结果
    result : 1 pass
                 2 error
                 3 fail
    :param reuslt:
    :return:
    """
    if result == 1:
        return "success"

    if result == 2:
        return "danger"
    if result == 3:
        return "danger"


@app_filter.app_template_filter("count_pass")
def count_pass(pass_cases, total_cases):
    return "%.2f%%" % (total_cases/pass_cases)


@app_filter.app_template_filter("filter_group_latest_result")
def filter_group_latest_result(group_id):
    report = Report.get_latest_by_group_id(group_id)
    if report is None:
        result = None
    else:
        result = Report.get_latest_by_group_id(group_id).result

    if result is True:
        return '<span class="fa fa-smile-o fa-lg " style="color: green"></span>'
    elif result is False:
        return '<span class="fa fa-frown-o fa-lg " style="color: red"></span>'
    else:
        return '<span class="fa fa-meh-o fa-lg "></span>'


@app_filter.app_template_filter("filter_group_latest_time")
def filter_group_latest_time(group_id):
    report = Report.get_latest_by_group_id(group_id)
    if report is None:
        time = u"尚未运行"
    else:
        time = report.datachange_createtime
    return time
