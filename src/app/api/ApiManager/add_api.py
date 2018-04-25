from flask import request, render_template

from src.app.api import api
from src.app.handler import register


@register(api, "/api", methods=["GET"])
def api_add():
    # data = request.form
    return render_template("index.html")