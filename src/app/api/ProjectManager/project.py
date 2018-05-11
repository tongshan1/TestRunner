from flask import request, redirect, url_for

from app import db
from module.Project import Project
from app.api import api
from app.form.project_form import ProjectFrom
from app.handler import register

import logging


def get_all_project():
    projects = Project.query.all()
    return projects


@register(api, "/project", methods=["POST"])
def project_add():
    project_form = ProjectFrom()
    if project_form.validate_on_submit():
        project = Project(
            project_name=project_form.project_name.data,
            project_testers=project_form.project_testers.data,
            project_developer=project_form.project_developer.data,
            project_version=project_form.project_version.data,
            project_desc=project_form.project_desc.data,
            is_active=project_form.is_active.data,
        )

        db.session.add(project)
        db.session.commit()
    else:
        logging.error(project_form.errors)

    return redirect("/")

