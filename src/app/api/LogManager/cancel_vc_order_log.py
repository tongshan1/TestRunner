# -*- coding: utf-8 -*-

from flask import render_template, request
from module.cancel_vc_order_log import CancelVcOrderLog
from app.api import api
from app.handler import register
import pymssql
import setting
import json


@register(api, "/cancel_vc_order_logs.html", methods=["GET"])
def cancel_vc_order_log_list():
    page = request.args.get('page', 1, type=int)
    pagination = CancelVcOrderLog.query.paginate(page, error_out=False)
    logs = pagination.items
    return render_template("cancel_vc_order_logs/index.html", pagination=pagination, logs=logs)


@register(api, "/cancel_vc_order_logs/<id>", methods=["GET"])
def cancel_vc_order_log_list_detail(id):
    log = CancelVcOrderLog.query.get(id)

    conn = pymssql.connect(host=setting.CAR_PRODUCT_UAT_SERVER,
                           port=int(setting.CAR_PRODUCT_UAT_PORT),
                           user=setting.CAR_ORDER_UID,
                           charset="utf8",
                           password=setting.CAR_ORDER_PWD)

    cursor = conn.cursor(as_dict=True)
    cursor.execute("select OrderId,requestcontent,responsecontent,apirequestcontent,apiresponsecontent,errmsg from LOG_ConnectLog where OrderId={order_id} and operatetype=1".format(order_id=log.order_id))
    detail = cursor.fetchone()
    return render_template("cancel_vc_order_logs/detail.html", log=log, detail=json.dumps(detail))


