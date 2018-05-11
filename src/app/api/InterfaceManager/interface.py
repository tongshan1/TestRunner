from flask import request, redirect

from app import db
from module.Interface import Interface
from app.api import api
from app.handler import register
from .request.request import api_request
from app.form.interface_form import InterfaceFrom


def get_all_interface():
    interfaces = Interface.query.all()
    return interfaces


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
        return redirect("/interface_list.html")
    else:
        print(interface_form.errors)

    return "2"


@register(api, "/api/<api_id>")
def interface_edit(api_id):
    print(api_id)
    return redirect("/")


@register(api, "/api/run", methods=["POST"])
def interface_request():
    interface_url = request.form.get("interface_url")
    interface_method = request.form.get("interface_method")
    interface_header = eval(request.form.get("interface_header"))
    interface_body = eval(request.form.get("interface_body").replace("true", "True").replace("false", "False"))

    response = api_request.request(interface_method, interface_url, headers=interface_header, json=interface_body)

    return response

