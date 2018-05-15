# -*- coding: utf-8 -*-

from flask import render_template

from app.api import api
from app.handler import register


@register(api, "/test_case", methods=["GET"])
def test_case_add():
    return render_template("test_cases/test_case_add.html")