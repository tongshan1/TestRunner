# -*- coding: utf-8 -*-
from flask import jsonify, render_template
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    return jsonify({403: 'Forbidden'}), 403


@main.app_errorhandler(404)
def page_not_found(e):
     return render_template("error/404.html")


@main.app_errorhandler(405)
def page_not_allowed(e):
    return jsonify({405: 'NotAllowed'}), 405


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template("error/500.html")
