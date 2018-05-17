# -*- coding: utf-8 -*-

from flask import render_template, request

from app.api import api
from app.handler import register
from app.api.ModuleManager.module import get_all_modules
from app.form.test_case_from import TestCaseFrom
from flask_wtf.csrf import generate_csrf


@register(api, "/test_case", methods=["GET", "POST"])
def test_case_add():
    if request.method == 'GET':
        return render_template("test_cases/test_case_add.html", modules=get_all_modules(), csrf_token=generate_csrf())
    else:
        test_case_from = TestCaseFrom()
