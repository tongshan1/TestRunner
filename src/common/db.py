# import psycopg2
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# https://vsupalov.com/flask-sqlalchemy-postgres/

#
# def get_env_variable(key):
#
#     try:
#         return os.environ[key]
#     except KeyError:
#         message = "No this key in environ"
#         raise Exception(message)

db_name = "TestRunner"
db_user = "postgres"
db_pass = "Shan84109649"
db_url = "127.0.0.1:5432"

DB_URL = 'postgres+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_user, pw=db_pass, url=db_url, db=db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


