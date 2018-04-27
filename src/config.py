import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))


class Config:


    SQLALCHEMY_DATABASE_URI = ''
    # SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SERVICE_VERSION = 'dev'


config = Config