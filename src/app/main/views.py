# -*- coding: utf-8 -*-
from . import main

from flask import Flask, render_template, request, redirect


@main.route("/login")
def login():
    return render_template("login.html")


@main.route('/')
@main.route('/index')
@main.route('/index.html')
def index():
    return render_template("index.html")


@main.route("/timer.html")
def timer():
    return render_template("timer.html")


