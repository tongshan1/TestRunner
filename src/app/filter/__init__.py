from flask import Blueprint

app_filter = Blueprint('app_filter', __name__)

from .report_filter import filter_result
from .report_filter import filter_testcase_class
from .report_filter import filter_testcase_result
from .report_filter import filter_group_latest_result
from .report_filter import filter_group_latest_time
from .test_case_filter import set_test_case_json_data
from .test_case_filter import set_test_case_data
