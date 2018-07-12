# -*- coding: utf-8 -*-


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
from jac.contrib.flask import JAC
from celery import Celery

from config import config, ROOT_PATH
from .logger import logger

logger = logger
db = SQLAlchemy()
celery = Celery(__name__, broker=config.CELERY_BROKER_URL)
cache = Cache()


app = Flask(__name__, root_path=ROOT_PATH)


def create_app():
    app.config.from_object(config)

    db.init_app(app)
    cache.init_app(app)

    JAC(app)

    celery.conf.update(app.config)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.views import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from app.filter import app_filter as app_filter_blueprint
    app.register_blueprint(app_filter_blueprint)

    return app