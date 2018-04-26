from flask import request, render_template

from src.app.api import api
from src.app.handler import register


@register(api, "/api", methods=["POST"])
def api_add():
    data = request.form.get("interface_name")
    return data