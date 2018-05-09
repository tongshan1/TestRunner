from flask import request, render_template

from app import db
from module.Interface import Interface
from app.api import api
from app.handler import register
from app.logger import debug
from .request.request import api_request


@register(api, "/api", methods=["POST"])
def interface_add():

    data = request.form
    # interface_name = request.form.get("interface_name")
    # interface_project= request.form.get("interface_project")
    # interface_url= request.form.get("interface_url")
    # interface_method= request.form.get("interface_method")
    # headers= request.form.get("headers")
    # params = request.form.get("params")

    interface = Interface(**data)
    db.session.add(interface)
    db.session.commit()
    return "1"


@register(api, "/api/run", methods=["POST"])
def interface_request():
    interface_url = request.form.get("interface_url")
    interface_method = request.form.get("interface_method")
    interface_header = request.form.get("interface_header")
    interface_body = request.form.get("interface_body")

    response = api_request.request(interface_method, interface_url)

    return response

