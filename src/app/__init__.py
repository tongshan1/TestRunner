# -*- coding: utf-8 -*-


from config import config, ROOT_PATH
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__, root_path=ROOT_PATH)


def create_app():
    app.config.from_object(config)

    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app


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



