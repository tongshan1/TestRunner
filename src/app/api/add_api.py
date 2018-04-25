from flask import request, render_template

from src.app.api import api
from src.app.handler import register


@register(api, "/api", methods=["GET"])
def api_add():
    if request.method == "GET":
        return render_template("create_api.html")