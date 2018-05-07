from flask import request, redirect

from app import db
from module.Project import Project
from app.api import api
from app.handler import register
from app.logger import debug


def get_all_project():
    projects = Project.query.all()
    return projects


@register(api, "/project", methods=["POST"])
def project_add():

    return redirect("/")

