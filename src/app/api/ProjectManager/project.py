# -*- coding: utf-8 -*-

from flask import request, redirect, flash, render_template
from app import db
from module.Project import Project
from app.api import api
from app.form.project_form import ProjectForm
from app.handler import register


def get_all_project():
    return Project.query.all()


@register(api, "/projects.html")
def project():
    projects = get_all_project()
    return render_template("projects/index.html", projects=projects, form=ProjectForm())


@register(api, "/project", methods=["POST"])
def project_create():
    form = ProjectForm(request.form)
    if form.validate():
        project_obj = Project()
        form.populate_obj(project_obj)
        db.session.add(project_obj)
        db.session.commit()
        flash(u'添加成功', category='success')
        return redirect("/projects.html")
    else:
        projects = get_all_project()
        flash(u'添加失败', category='danger')
        return render_template("projects/index.html", projects=projects, form=form, modal_display=True)


@register(api, "/projects/<id>/edit", methods=["GET"])
def project_edit(id):
    project_obj = Project.query.get(id)
    form = ProjectForm(obj=project_obj)
    return render_template("projects/edit.html", form=form)


@register(api, "/projects/<id>/update", methods=["POST"])
def project_update(id):
    form = ProjectForm(request.form)
    if form.validate():
        project_obj = Project.query.get(id)
        form.populate_obj(project_obj)
        db.session.add(project_obj)
        db.session.commit()
        flash(u'更新成功', category='success')
        return redirect("/projects.html")
    else:
        flash(u'更新失败', category='danger')
        return redirect("/projects.html")
