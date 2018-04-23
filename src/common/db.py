import psycopg2
import os
from flask import app
from flask_sqlalchemy import SQLAlchemy


# https://vsupalov.com/flask-sqlalchemy-postgres/


def get_env_variable(key):

    try:
        return os.environ[key]
    except KeyError:
        message = "No this key in environ"
        raise Exception(message)

db_name = get_env_variable("POSTGRES_DB")
db_user = get_env_variable("POSTGRES_USER")
db_pass = get_env_variable("POSTGRES_PW")
db_url = get_env_variable("POSTGRES_URL")

DB_URL = 'postgres+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_user, pw=db_pass, url=db_url, db=db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
