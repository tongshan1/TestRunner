from flask import request, redirect, render_template, jsonify
import json

from app import db
from module.Interface import Interface
from schema.interface import InterfaceSchema
from app.api import api
from app.handler import register, success, fail
from app.api.ModuleManager.module import get_all_modules
from .request.request import api_request
from app.form.interface_form import InterfaceFrom
from flask_wtf.csrf import generate_csrf


def get_all_interface():
    interfaces = Interface.query.all()
    return interfaces


@register(api, "/interface", methods=["POST"])
def interface_add():

    interface_form = InterfaceFrom()

    if interface_form.validate_on_submit():
        interface = Interface(
            interface_name=interface_form.interface_name.data,
            module_id = interface_form.module_id.data,
            interface_url=interface_form.interface_url.data,
            interface_header=interface_form.interface_header.data,
            interface_body=interface_form.interface_body.data,
            interface_method=interface_form.interface_method.data,
            is_active=interface_form.is_active.data
        )
        db.session.add(interface)
        db.session.commit()
        return success()
    else:
        return fail(2, error=interface_form.errors)


@register(api, "/interface/module/<module_id>")
def get_interface_by_module(module_id):
    interfaces = Interface.query.filter(Interface.module_id==module_id).all()
    interfaces = InterfaceSchema(many=True).dumps(interfaces)

    return interfaces


@register(api, "/interface/<interface_id>", methods=["GET"])
def interface_by_id(interface_id):
    interface_obj = Interface.query.filter(Interface.id == interface_id).one()
    interface_obj = InterfaceSchema().dumps(interface_obj)

    return interface_obj


@register(api, "/interface_list.html", methods=["GET"])
def interface_list():
    return render_template("interface/list.html", interfaces=get_all_interface())


@register(api, "/interface.html", methods=['GET'])
def interface():
    return render_template("interface/new.html", csrf_token=generate_csrf(), modules=get_all_modules())


@register(api, "/interface/run", methods=["POST"])
def interface_request():
    interface_url = request.form.get("interface_url")
    interface_method = request.form.get("interface_method")
    interface_header = eval(request.form.get("interface_header"))
    interface_body = eval(request.form.get("interface_body").replace("true", "True").replace("false", "False"))

    response = api_request.request(interface_method, interface_url, headers=interface_header, json=interface_body)

    return response

