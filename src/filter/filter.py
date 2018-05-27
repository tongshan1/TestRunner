
def filter_result(result):
    """

    :param key:
    :return:
    """
    if result:
        return u"成功"
    else:
        return u"失败"

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

def filter_testcase_class(reuslt):
    """
    过滤测试结果
    result : 1 pass
                 2 error
                 3 fail
    :param reuslt:
    :return:
    """
    if reuslt == 1:
        return "success"

    if reuslt == 2:
        return "danger"
    if reuslt == 3:
        return "danger"

def count_pass(pass_cases, total_cases):
    return "%.2f%%" % (total_cases/pass_cases)
