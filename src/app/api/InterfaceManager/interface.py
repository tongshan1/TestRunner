from flask import request, render_template

from app import db
from module.Interface import Interface
from app.api import api
from app.handler import register
from .request.request import api_request
from app.form.interface_form import InterfaceFrom

import json


@register(api, "/api", methods=["POST"])
def interface_add():

    interface_form = InterfaceFrom()

    if interface_form.validate_on_submit():
        interface = Interface(
            interface_name=interface_form.interface_name.data,
            interface_url=interface_form.interface_url.data,
            interface_header=interface_form.interface_header.data,
            interface_body=interface_form.interface_body.data,
            interface_method=interface_form.interface_method.data,
            is_active=interface_form.is_active.data
        )
        db.session.add(interface)
        db.session.commit()
        return "1"
    else:
        print(interface_form.errors)

    return "2"


@register(api, "/api/run", methods=["POST"])
def interface_request():
    interface_url = request.form.get("interface_url")
    interface_method = request.form.get("interface_method")
    interface_header = eval(request.form.get("interface_header"))
    interface_body = eval(request.form.get("interface_body"))

    response = api_request.request(interface_method, interface_url, headers=interface_header, json=interface_body)

    return response

