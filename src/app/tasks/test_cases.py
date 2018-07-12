# -*- coding: utf-8 -*-
from app import celery
from app.logger import logger
from utils.TestCase.all_tests import AllTests


@celery.task(bind=True)
def run_interface_case(self, test_group_id):
    all_test = AllTests()
    all_test.run_case(self, test_group_id)
