# -*- coding: utf-8 -*-
from flask import render_template

from app.views import api
from app.handler import register


@register(api, "/timed_task.html")
def timed_task():
    return render_template("timed_task/index.html")