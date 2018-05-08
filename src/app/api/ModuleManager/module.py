from flask import request, redirect, url_for

from app import db
from module.Module import Module
from app.api import api
from app.form.module_form import ModuleFrom
from app.handler import register

import logging


def get_all_module():
    modules = Module.query.all()
    return modules


@register(api, "/module", methods=["POST"])
def module_add():
    module_form = ModuleFrom()
    if module_form.validate_on_submit():
        module = Module(
            module_name=module_form.module_name.data,
            project_id = module_form.project_id.data,
            module_testers=module_form.module_testers.data,
            module_developer=module_form.module_developer.data,
            module_version=module_form.module_version.data,
            module_desc=module_form.module_desc.data,
            is_active=module_form.is_active.data,
        )

        db.session.add(module)
        db.session.commit()
    else:
        logging.error(module_form.errors)

    return redirect("/")


