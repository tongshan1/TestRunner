import os
from flask import request, redirect, render_template, flash, url_for, send_from_directory, current_app
from flask_wtf.csrf import generate_csrf

from app import db
from app.api import api
from app.api.ModuleManager.module import get_all_modules
from app.handler import register, success, fail
from app.form.interface_form import InterfaceFrom
from app.logger import logger

from module.Interface import Interface
from module.System_setting import SystemSetting
from schema.interface import InterfaceSchema
from .request.request import api_request
from .utils.insert_swagger import insert_data


@register(api, "/interface.html", methods=['GET'])
def interface():
    return render_template("interface/new.html", csrf_token=generate_csrf(), modules=get_all_modules(),
                           runner_setting=SystemSetting.get_runner_setting())


@register(api, "/interface", methods=["POST"])
def interface_add():
    interface_form = InterfaceFrom(request.form)

    logger.error(request.form)
    if interface_form.validate():
        interface_obj = Interface()
        interface_form.populate_obj(interface_obj)
        db.session.add(interface_obj)
        db.session.commit()
        return success()
    else:
        return fail(2, error=str(interface_form.errors))


@register(api, "/interface/module/<module_id>")
def get_interface_by_module(module_id):
    interfaces = Interface.query.filter(Interface.module_id == module_id).all()
    interfaces = InterfaceSchema(many=True).dumps(interfaces)

    return interfaces


@register(api, "/interface/<interface_id>", methods=["GET"])
def interface_by_id(interface_id):
    interface_obj = Interface.get_by_id(interface_id)
    interface_obj = InterfaceSchema().dumps(interface_obj)

    return interface_obj


@register(api, "/interface/<interface_id>/edit", methods=["GET", "POST"])
def interface_edit(interface_id):
    interface_obj = Interface.get_by_id(interface_id)
    if request.method == "GET":
        return render_template("interface/edit.html", interface=interface_obj, csrf_token=generate_csrf(),
                               modules=get_all_modules())
    else:
        interface_form = InterfaceFrom(request.form)
        if interface_form.validate():
            interface_obj = Interface.get_by_id(interface_id)
            interface_form.populate_obj(interface_obj)
            db.session.add(interface_obj)
            db.session.commit()
            return success()
        else:
            return fail(2, error=str(interface_form.errors))


@register(api, "/interface_list.html", methods=["GET"])
def interface_list():
    return render_template("interface/list.html", interfaces=Interface.get_all_oder_by_module())


@register(api, "/interface/run", methods=["POST"])
def interface_request():
    runner_setting = request.form.get("setting")
    interface_url = request.form.get("interface_url")
    interface_method = request.form.get("interface_method")
    interface_header = request.form.get("interface_header")
    interface_body = request.form.get("interface_body")
    interface_query = request.form.get("interface_query")
    testcase_verification = request.form.get("testcase_verification")

    response, result = api_request.request(interface_method, interface_url, headers=interface_header,
                                           data=interface_body, testcase_verification=testcase_verification,
                                           params=interface_query, runner_setting=runner_setting)

    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@register(api, "/interface/import", methods=["POST"])
def interface_import():
    if 'interface_file' not in request.files:
        flash('没有文件上传文件', category='danger')
        return redirect("/interface_list.html")
    file = request.files['interface_file']
    if file.filename == '':
        flash('没有选中文件！', category='danger')
        return redirect("/interface_list.html")
    if file and allowed_file(file.filename):
        insert_data(file)
        flash('导入成功', category='success')
        return redirect("/interface_list.html")
    else:
        flash('导入失败', category='success')
        return redirect("/interface_list.html")
