# -*- coding: utf-8 -*-


from config import config, ROOT_PATH
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from celery import Celery
from jac.contrib.flask import JAC


db = SQLAlchemy()

app = Flask(__name__, root_path=ROOT_PATH)


def create_app():
    app.config.from_object(config)

    db.init_app(app)
    JAC(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from app.filter import app_filter as app_filter_blueprint
    app.register_blueprint(app_filter_blueprint)

    return app


# def make_celery():
#     app = create_app()
#     celery = Celery(app.import_name,
#                     backend=app.config['CELERY_RESULT_BACKEND'],
#                     broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#
#     class ContextTask(TaskBase):
#         abstract = True
#
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
#
#
# celery = make_celery()

# @app.before_first_request
# def set_up_logging():
#     from app.logger import LogFormatter
#     logging.getLogger("werkzeug").disabled = True
#
#     app.logger.setLevel(logging.DEBUG)
#     if not app.debug:
#         app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)
#
#     for hdl in app.logger.handlers:
#         hdl.setFormatter(LogFormatter(color=hdl.level == logging.DEBUG))
