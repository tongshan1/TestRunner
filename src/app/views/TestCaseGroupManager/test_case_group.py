from flask import redirect, render_template, flash, request
from flask_wtf.csrf import generate_csrf
from celery.result import AsyncResult

from app import db, celery
from app.module.TestCaseGroup import Testcasegroup
from app.module.TestCaseTestGroup import Testcase_testgroup
from app.views import api
from app.handler import register, success, fail
from app.form.testcase_group_form import TestCaseGroupForm
from app.form.testcase_testgoup_from import TestCaseTestGroupForm
from app.views.ModuleManager.module import get_all_modules
from app.logger import logger
from .util import get_testcase_by_group_id
from app.tasks.test_cases import run_interface_case


@register(api, "/testcase_group.html", methods=["GET", "POST"])
def testcase_group():
    if request.method == "GET":
        return render_template("test_cases/test_group.html", form=TestCaseGroupForm(), testcase_groups=Testcasegroup.get_all())
    else:
        testcase_group_form = TestCaseGroupForm(request.form)
        target = request.referrer
        if testcase_group_form.validate():
            testcase_group_obj = Testcasegroup()
            testcase_group_form.populate_obj(testcase_group_obj)
            db.session.add(testcase_group_obj)
            db.session.commit()
            flash(u'添加成功', category='success')
        else:
            flash(u'添加失败', category='danger')

        return redirect(target)


@register(api, "/testcase_group/<test_group_id>/test_group_edit.html", methods=["GET", "POST"])
def testcase_group_edit(test_group_id):
    if request.method == "GET":
        testcase_group = Testcasegroup.get_by_id(test_group_id)

        testcase_group_from = TestCaseGroupForm(obj=testcase_group)
        testcase_testgroups = get_testcase_by_group_id(test_group_id)

        return render_template("test_cases/test_group_edit.html", form=testcase_group_from, testcase_testgroups=testcase_testgroups,
                            modules=get_all_modules(), csrf_token=generate_csrf())
    else:
        form = TestCaseGroupForm(request.form)
        if form.validate():
            testcase_group_obj = Testcasegroup.query.get(test_group_id)
            form.populate_obj(testcase_group_obj)
            db.session.add(testcase_group_obj)
            db.session.commit()
            flash(u'更新成功', category='success')
            return redirect("/testcase_group/{0}/test_group_edit.html".format(test_group_id))
        else:
            print(form.errors)
            flash(u'更新失败', category='danger')
            return redirect("/testcase_group/{0}/test_group_edit.html".format(test_group_id))


@register(api, "/testcase_testgroup", methods=["POST"])
def testcase_testgroup_add():
    testcase_testgroup_from = TestCaseTestGroupForm()

    if testcase_testgroup_from.validate_on_submit():
        # 先获取group id 看看一共有多少testcase 在设置执行顺序
        testcase_group_id = testcase_testgroup_from.testcase_group_id.data
        testcase_len = len(get_testcase_by_group_id(testcase_group_id))

        testcase_test_group_obj = Testcase_testgroup()
        testcase_testgroup_from.populate_obj(testcase_test_group_obj)
        testcase_test_group_obj.testcase_execution_order = (testcase_len+1)
        db.session.add(testcase_test_group_obj)
        db.session.commit()
        return success()
    else:
        return fail(ret=2)


@register(api, "/testcase_testgroup/<id>/delete", methods=["DELETE"])
def testcase_testgroup_delete(id):
    testcase_testgroup = Testcase_testgroup.query.get(id)

    testcase_testgroup.is_active = False

    db.session.add(testcase_testgroup)
    db.session.commit()
    return success()


@register(api, "/testgroup/<test_group_id>/run", methods=["POST"])
def testgroup_run(test_group_id):
    task = run_interface_case.delay(test_group_id)

    return success({"task_id": task.id})


@register(api, "/testgroup/<task_id>/status")
def testgroup_status(task_id):

    task = AsyncResult(task_id, app=celery)

    if task.state == "PENDING":
        return success({'state': task.state, 'current': 0, 'total': 1})
    elif task.state == "PROGRESS":
        return success({'state': task.state, 'current': task.info.get("current"), 'total': task.info.get("total")})
    else:

        report_id = task.get()
        logger.error(report_id)
        return success({'state': task.state, 'current': 1, 'total': 1, 'report':report_id})



