import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))


class Config:

    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 60*60
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True

    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:Shan84109649@127.0.0.1:5432/TestRunner'
    SQLALCHEMY_BINDS = {}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SERVICE_VERSION = 'dev'

    DATABASE_QUERY_TIMEOUT = 0.005
    SQLALCHEMY_RECORD_QUERIES = True


config = {
    'development': DevelopmentConfig,

}