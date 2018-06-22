
from flask import render_template

from module.Interface import Interface
from module.Testcase import TestInterfacecase
from app.api import api
from app.handler import register


@register(api, "/index.html")
def index():
    data = {}
    interface=len(Interface.get_all())
    testcase = len(TestInterfacecase.get_all())

    data["interface"] = interface
    data["testcase"] = testcase
    return render_template("index.html", data=data)