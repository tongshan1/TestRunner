
import json
from flask import request, redirect, render_template, flash, url_for, current_app

from app import db
from app.api import api
from app.handler import register, success, fail
from app.form.interface_form import InterfaceFrom, populate_interface
from app.logger import logger

from module.Interface import Interface
from schema.interface import InterfaceSchema
from .request.request import api_request
from .utils.insert_swagger import insert_data


def init_field_data(field):
    field_data = []
    for v in field:
        data = {}
        data["name"] = v.get("key")
        data["value"] = v.get("value")
        data["description"] = v.get("desc")
        field_data.append(data)
    return field_data


@register(api, "/interface.html", methods=['GET', "POST"])
def interface():
    if request.method == "GET":
        form = InterfaceFrom()
        return render_template("interface/interface.html", title=u"添加", form=form)
    else:
        form = InterfaceFrom(request.form)
        if form.validate():
            interface_obj = Interface()
            interface_obj.interface_url = form.interface_url.data
            interface_obj.interface_name = form.interface_name.data
            interface_obj.module = form.module.data
            interface_obj.interface_method = form.interface_method.data
            interface_obj.interface_desc = form.interface_desc.data
            interface_obj.interface_header = init_field_data(form.interface_header.data)
            interface_obj.interface_query = init_field_data(form.interface_query.data)

            data_type = request.form.get("data_type")
            if data_type == "JSON_data_select":
                interface_obj.interface_body = json.loads(form.interface_json.data)
            else:
                interface_obj.interface_body = init_field_data(form.interface_data.data)

            db.session.add(interface_obj)
            db.session.commit()
            return success()
        else:
            logger.error(form.errors)
            return fail(2, error=form.errors)


@register(api, "/interface/<interface_id>/edit.html", methods=["GET", "POST"])
def interface_edit(interface_id):
    interface_obj = Interface.get_by_id(interface_id)
    form = populate_interface(interface_obj)
    if request.method == "GET":
        return render_template("interface/interface.html", title=u"编辑", form=form)
    else:
        form = InterfaceFrom(request.form)
        data_type = request.form.get("data_type")
        if form.validate():
            interface_obj = Interface.get_by_id(interface_id)
            interface_obj.interface_name = form.interface_name.data
            interface_obj.module = form.module.data
            interface_obj.interface_url = form.interface_url.data
            interface_obj.interface_desc = form.interface_desc.data
            interface_obj.interface_header = init_field_data(form.interface_header.data)
            interface_obj.interface_query = init_field_data(form.interface_query.data)

            logger.error(form.interface_data.data)
            if data_type == "JSON_data_select":
                interface_obj.interface_body = json.loads(form.interface_json.data)
            else:
                interface_obj.interface_body = init_field_data(form.interface_data.data)
            db.session.add(interface_obj)
            db.session.commit()
            return success()
        else:
            return fail(2, error=str(form.errors))


def init_run_field_data(field):
    data = {}
    for v in field:
        data[v.get("key")] = v.get("value")
    return data


@register(api, "/interface/run", methods=["POST"])
def interface_request():

    form = InterfaceFrom(request.form)

    runner_setting = form.runner_setting.data.id
    interface_url = form.interface_url.data
    interface_method = form.interface_method.data
    interface_header = init_run_field_data(form.interface_header.data)
    data_type = request.form.get("data_type")
    if data_type == "JSON_data_select":
        interface_body = form.interface_json.data
    else:
        interface_body = init_run_field_data(form.interface_data.data)

    interface_query = init_run_field_data(form.interface_query.data)

    response, result = api_request.request(interface_method, interface_url, headers=interface_header,
                                           data=interface_body, params=interface_query, runner_setting=runner_setting)

    return response


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


@register(api, "/interface_list.html", methods=["GET"])
def interface_list():
    return render_template("interface/list.html", interfaces=Interface.get_all_oder_by_module())


@register(api, "/interface/<interface_id>/delete", methods=["DELETE"])
def interface_delete(interface_id):
    interface_obj = Interface.get_by_id(interface_id)
    interface_obj.is_active = False
    db.session.add(interface_obj)
    db.session.commit()
    return success()


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
