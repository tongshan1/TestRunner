# -*- coding: utf-8 -*-
from . import main
from app.api.ProjectManager.project import get_all_project
from app.api.ModuleManager.module import get_all_module
from app.api.TestCaseGroupManager.test_case_group import get_all_testc_case_group
from app.form.project_form import ProjectFrom
from app.form.module_form import ModuleFrom
from app.form.testcase_group_form import TestCaseGroupForm
from flask_wtf.csrf import generate_csrf

from flask import Flask, render_template, request, redirect


@main.route("/login")
def login():
    return render_template("login.html")


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")


@main.route("/api.html", methods=['GET'])
def api():
    return render_template("add_interface.html", csrf_token=generate_csrf())


@main.route("/timer.html")
def timer():
    return render_template("timer.html")


@main.route("/projects.html")
def project():
    projects = get_all_project()
    return render_template("projects.html", projects=projects, form=ProjectFrom())


@main.route("/modules.html")
def module():
    modules = get_all_module()
    return render_template("modules.html", modules=modules, form=ModuleFrom())


@main.route("/testcase_group.html")
def testcase_group():
    testcase_groups = get_all_testc_case_group()
    return render_template("test_cases.html", testcase_groups=testcase_groups, form=TestCaseGroupForm())

@main.route("/test_case_detail.html")
def testcase_detail_group():

    return render_template("test_case_details.html")


