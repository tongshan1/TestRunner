# -*- coding: utf-8 -*-
from celery import current_app as app
from utils.TestCase.all_tests import AllTests


@app.task(name='interface_case.run', exchange='interface_case', ignore_result=True, routing_key='cases')
def run_interface_case(test_group_id):
    all_test = AllTests()
    all_test.run_case(test_group_id)