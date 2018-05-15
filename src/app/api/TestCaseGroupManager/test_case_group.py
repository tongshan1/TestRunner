from flask import redirect, render_template

from app import db
from module.Testcasegroup import Testcasegroup
from module.Testcase_testgroup import Testcase_testgroup
from module.Testcase import TestInterfacecase
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


@register(api, "/testcase_group/<id>/test_group_edit.html", methods=["GET"])
def testcase_group_edit(id):
    testcase_group = Testcasegroup.query.get(id)
    testcase_testgroups = Testcase_testgroup.query.filter_by(testcase_group_id=id)

    testcases = []
    if testcase_group.testcase_type == 1:

        for testcase_testgroup in testcase_testgroups:
            testcase_id = testcase_testgroup.testcase_id
            testcase = TestInterfacecase.query.get(testcase_id)
            testcases.append(testcase)

    return render_template("test_cases/test_group_edit.html", testcase_group=testcase_group, tescases=testcases)



