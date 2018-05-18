# -*- coding: utf-8 -*-

from flask import request, redirect, flash, render_template
from app import db
from module.Module import Module
from app.api import api
from app.form.module_form import ModuleForm
from app.handler import register

def get_all_modules():
    return Module.query.all()


@register(api, "/modules.html", methods=["GET"])
def module_list():
    modules = get_all_modules()
    return render_template("modules/index.html", modules=modules)


@register(api, "/modules/new", methods=["GET"])
def module_new():
    form = ModuleForm()
    return render_template("modules/new.html", form=form)


@register(api, "/modules/create", methods=["POST"])
def module_create():
    form = ModuleForm(request.form)
    if form.validate():
        module_obj = Module()
        form.populate_obj(module_obj)
        db.session.add(module_obj)
        db.session.commit()
        flash(u'添加成功', category='success')
        return redirect("/modules.html")
    else:
        flash(u'添加失败', category='danger')
        return render_template("modules/new.html", form=form)


@register(api, "/modules/<id>/edit", methods=["GET"])
def module_edit(id):
    module_obj = Module.query.get(id)
    form = ModuleForm(obj=module_obj)
    return render_template("modules/edit.html", form=form, module_obj=module_obj)


@register(api, "/modules/<id>/update", methods=["POST"])
def module_update(id):
    form = ModuleForm(request.form)
    module_obj = Module.query.get(id)
    if form.validate():
        form.populate_obj(module_obj)
        db.session.add(module_obj)
        db.session.commit()
        flash(u'更新成功', category='success')
        return redirect("/modules.html")
    else:
        flash(u'更新失败', category='danger')
        return render_template("modules/edit.html", form=form, module_obj=module_obj)
