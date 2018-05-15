# -*- coding: utf-8 -*-
from . import main
from app.api.TestCaseGroupManager.test_case_group import get_all_testc_case_group
from app.api.InterfaceManager.interface import get_all_interface
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
    return render_template("interface/new.html", csrf_token=generate_csrf())


@main.route("/interface_list.html")
def interface_list():
    interfaces = get_all_interface()
    return render_template("interface/list.html", interfaces=interfaces)


@main.route("/timer.html")
def timer():
    return render_template("timer.html")


@main.route("/testcase_group.html")
def testcase_group():
    testcase_groups = get_all_testc_case_group()
    return render_template("test_cases/test_cases.html", testcase_groups=testcase_groups, form=TestCaseGroupForm())

