from flask import request, redirect, render_template
from app.handler import register, success, fail
from app.api import api
from app.form.setting_form import RunnerSettingFrom

from module.System_setting import SystemSetting


@register(api, "/runner_setting_list.html")
def runner_setting():
    runner_setting = SystemSetting.get_runner_setting()
    return render_template("setting/runner_setting_list.html", runner_setting=runner_setting)


@register(api, "/runner_setting_new.html", methods=["GET", "POST"])
def runner_setting_new():
    form = RunnerSettingFrom()
    return render_template("setting/runner_setting_new.html", form=form)