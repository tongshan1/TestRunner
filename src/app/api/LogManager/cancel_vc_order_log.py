# -*- coding: utf-8 -*-

from flask import render_template
from module.cancel_vc_order_log import CancelVcOrderLog
from app.api import api
from app.handler import register


@register(api, "/cancel_vc_order_logs.html", methods=["GET"])
def cancel_vc_order_log_list():
    logs = CancelVcOrderLog.query.all()
    return render_template("cancel_vc_order_logs/index.html", logs=logs)


@register(api, "/cancel_vc_order_logs/<id>", methods=["GET"])
def cancel_vc_order_log_list_detail(id):
    log = CancelVcOrderLog.query.get(id)
    return render_template("cancel_vc_order_logs/detail.html", log=log)
