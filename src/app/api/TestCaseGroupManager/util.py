from module.Testcasegroup import Testcasegroup
from module.Testcase_testgroup import Testcase_testgroup


def get_testcase_group(group_id):
    return Testcasegroup.query.get(group_id)


def get_testcase_by_group_id(group_id):
    testcase_testgroups = Testcase_testgroup.query.filter_by(testcase_group_id=group_id, is_active=True).order_by(
        Testcase_testgroup.testcase_execution_order).all()

    return testcase_testgroups


def get_setting_runner_by_group_id(group_id):
    return Testcasegroup.get_by_id(group_id).runner_setting_id

