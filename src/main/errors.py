# -*- coding: utf-8 -*-
from flask import jsonify
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    return jsonify({403: 'Forbidden'}), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return jsonify({404: 'NotFound'}), 404


@main.app_errorhandler(405)
def page_not_allowed(e):
    return jsonify({405: 'NotAllowed'}), 405


@main.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({500: 'Error'}), 500
