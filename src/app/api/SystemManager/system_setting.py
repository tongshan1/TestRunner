from flask import request, redirect, render_template, flash
from app.handler import register, success, fail
from app.api import api
from app import db
from app.form.setting_form import SettingFrom, populate_setting

from module.System_setting import SystemSetting

from app.logger import logger


@register(api, "/runner_setting_list.html")
def runner_setting_list():
    runner_setting = SystemSetting.get_runner_setting()
    return render_template("setting/runner_setting_list.html", runner_setting=runner_setting)


def init_setting_value(value):
    data = {}
    for v in value:
        key = v.get("key")
        value = v.get("value")
        data[key] = value
    return data


@register(api, "/runner_setting_new.html", methods=["GET", "POST"])
def runner_setting_new():
    if request.method == "GET":

        form = SettingFrom()
        return render_template("setting/runner_setting_new.html", form=form, title=u"新增")
    else:
        form = SettingFrom(request.form)
        target = request.referrer
        if form.validate():
            setting_obj = SystemSetting()
            setting_obj.key = form.key.data
            setting_obj.value = init_setting_value(form.value.data)
            setting_obj.desc = form.desc.data
            setting_obj.type = 1
            db.session.add(setting_obj)
            db.session.commit()
            flash(u'添加成功', category='success')
            return redirect("/runner_setting_list.html")
        else:
            flash(form.errors, category='danger')
            return redirect(target)


@register(api, "/setting/<setting_id>/setting_edit.html", methods=["GET", "POST"])
def runner_setting_edit(setting_id):
    setting = SystemSetting.get_by_id(setting_id)
    if setting is None:
        return render_template("error/404.html")

    if request.method == "GET":
        form = populate_setting(setting)
        return render_template("setting/runner_setting_new.html", form=form, title=u"更新")
    else:
        # 更新
        form = SettingFrom(request.form)
        target = request.referrer
        if form.validate():
            setting.key = form.key.data
            setting.desc = form.desc.data
            setting.value = init_setting_value(form.value.data)
            db.session.add(setting)
            db.session.commit()
            flash(u'更新成功', category='success')
        else:
            flash(form.errors, category='danger')
        return redirect(target)


@register(api, "/setting/<setting_id>/default")
def runner_setting_default(setting_id):

    default_setting = SystemSetting.get_default_runner_setting()

    for setting in default_setting:
        setting.is_default = False
        db.session.add(setting)
    runner_setting = SystemSetting.get_by_id(setting_id)
    runner_setting.is_default = True
    db.session.add(runner_setting)
    db.session.commit()
    return success()
