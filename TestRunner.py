from flask import Flask, render_template
from src.common.generate_code import generate_code

app = Flask(__name__)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/api")
def api():
    return render_template("create_api.html")


@app.route("/doc")
def show_swagger():
    return render_template("swagger.html", tag_data=generate_code())

if __name__ == '__main__':
    app.run()
