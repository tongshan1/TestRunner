# -*- coding: utf-8 -*-
from . import main

from flask import Flask, render_template, request, redirect


@main.route("/login")
def login():
    return render_template("login.html")


@main.route('/')
def index():
    return render_template("index.html")


@main.route("/api.html", methods=['GET'])
def api():
    return render_template("create_api.html")


@main.route("/timer")
def timer():
    return render_template("timer.html")


@main.route("/projects")
def projects():
    return render_template("projects.html")


@main.route("/modules")
def modules():
    return render_template("modules.html")


