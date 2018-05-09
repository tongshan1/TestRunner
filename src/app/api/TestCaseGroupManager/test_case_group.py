from flask import redirect

from app import db
from module.Testcasegroup import Testcasegroup
from app.api import api
from app.handler import register
from app.form.testcase_group_form import TestCaseGroupForm
import logging


def get_all_testc_case_group():
    testcase_group = Testcasegroup.query.all()
    return testcase_group


@register(api, "/testcase_group", methods=["POST"])
def testcase_group_add():

    testcase_group_form = TestCaseGroupForm()
    if testcase_group_form.validate_on_submit():
        project = Testcasegroup(
            testcase_group_name=testcase_group_form.testcase_group_name.data,
            module_id=testcase_group_form.module_id.data,
            testcase_type=testcase_group_form.testcase_type.data,
            testcase_desc=testcase_group_form.testcase_desc.data,
            is_active=testcase_group_form.is_active.data,
        )

        db.session.add(project)
        db.session.commit()
    else:
        logging.error(testcase_group_form.errors)

    return redirect("/")

