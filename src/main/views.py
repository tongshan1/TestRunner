# -*- coding: utf-8 -*-
from . import main

from flask import Flask, render_template, request, redirect


@main.route("/login")
def login():
    return render_template("login.html")


@main.route('/')
def index():
    return render_template("index.html")


# @main.route("/api", methods=['GET', 'POST'])
# def api():
#     if request.method == "GET":
#         return render_template("create_api.html")
#     else:
#         return redirect("/api/doc")


@main.route("/timer")
def timer():
    return render_template("timer.html")


# @main.route("/api/doc")
# def show_swagger():
#     return render_template("api_doc.html", tag_data=generate_code())


