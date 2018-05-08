# -*- coding: utf-8 -*-
from . import main
from app.api.ProjectManager.project import get_all_project
from app.api.ModuleManager.module import get_all_module
from app.form.project_form import ProjectFrom
from app.form.module_form import ModuleFrom

from flask import Flask, render_template, request, redirect


@main.route("/login")
def login():
    return render_template("login.html")


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")


@main.route("/api.html", methods=['GET'])
def api():
    return render_template("create_api.html")


@main.route("/timer.html")
def timer():
    return render_template("timer.html")


@main.route("/projects.html")
def project():
    projects = get_all_project()
    return render_template("projects.html", projects=projects, form=ProjectFrom())


@main.route("/modules.html")
def module():
    modules = get_all_module()
    return render_template("modules.html", modules=modules, form=ModuleFrom())


